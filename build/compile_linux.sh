#!/usr/bin/env bash
set -e

# Change directory to repo root
cd "$(dirname "$0")/.."

echo "=== Building Toontown Archipelago Linux Release ==="

PYTHON="${PYTHON:-python3}"

echo "Checking Python version..."
$PYTHON --version

echo "Installing build requirements..."
$PYTHON -m pip install --upgrade pip 2>/dev/null || true
$PYTHON -m pip install nuitka
$PYTHON -m pip install -r requirements.txt

# Check if Panda3D is installed
if ! $PYTHON -c "import panda3d" 2>/dev/null; then
    # Check if a local wheel is present in current directory, dist, or parent
    LOCAL_WHL=$(find . /dist .. -maxdepth 2 -name "panda3d*.whl" 2>/dev/null | head -n 1)
    if [ -n "$LOCAL_WHL" ]; then
        echo "Installing local Panda3D wheel: $LOCAL_WHL"
        $PYTHON -m pip install "$LOCAL_WHL"
    else
        echo "Panda3D not found. Installing prebuilt wheel from GitHub..."
        $PYTHON -m pip install "https://github.com/toontown-archipelago/panda3d/releases/latest/download/panda3d-1.11.0-cp311-cp311-linux_x86_64.whl" || {
            echo "Failed to install Panda3D wheel. Please build or install panda3d first."
            exit 1
        }
    fi
fi

echo "Compiling standalone client with Nuitka..."
$PYTHON -m nuitka ./launch/launcher/launch.py \
    --standalone \
    --output-dir=output \
    --include-package=direct.distributed \
    --include-package=otp \
    --include-package=toontown \
    --include-package-data=panda3d \
    --assume-yes-for-downloads

echo "Building APWorld..."
(cd apworld && bash make_apworld.sh)

echo "Assembling release directory..."
rm -rf release
mkdir -p release/game

cp -r output/launch.dist/* release/game/
if [ -f release/game/launch.bin ]; then
    mv release/game/launch.bin release/game/launch
fi
chmod +x release/game/launch

# Copy Panda3D DSO plugins and PRC files into release/game
PANDA_DIR=$($PYTHON -c "import panda3d, os; print(os.path.dirname(panda3d.__file__))")
echo "Panda3D package directory: $PANDA_DIR"
cp -P "$PANDA_DIR"/*.so* release/game/ 2>/dev/null || true
if [ -d "$PANDA_DIR/etc" ]; then
    mkdir -p release/game/etc
    cp -r "$PANDA_DIR"/etc/* release/game/etc/
fi

echo "Copying apworld definitions..."
mkdir -p release/game/apworld/toontown
cp apworld/toontown/archipelago.json release/game/apworld/toontown/

echo "Packing resources with multify..."
mkdir -p release/game/resources
MULTIFY_BIN="$(which multify 2>/dev/null || echo "$(dirname "$($PYTHON -c 'import sys; print(sys.executable)')")/multify")"
(
    cd resources
    for dir in */; do
        "$MULTIFY_BIN" -c -f "../release/game/resources/${dir%/}.mf" "${dir%/}"
    done
)

echo "Copying config files..."
mkdir -p release/game/config
cp config/production.prc release/game/config/
cp config/common.prc release/game/config/

echo "Copying Linux launch scripts..."
cp build/scripts/*.sh release/
chmod +x release/*.sh

echo "Copying Astron server..."
cp -r astron release/game
chmod +x release/game/astron/astrond-linux* 2>/dev/null || true

# Include transitive dependencies of Panda3D and its plugins, not just known codecs.
# Keep glibc and graphics driver libraries supplied by the user's system.
while IFS= read -r -d '' binary; do
    while read -r name arrow library rest; do
        [ "$arrow" = '=>' ] && [ -f "$library" ] || continue
        case "$name" in
            libc.so.*|libm.so.*|libmvec.so.*|libpthread.so.*|libdl.so.*|librt.so.*|libresolv.so.*|libutil.so.*|ld-linux*|libGL*.so*|libEGL.so*|libOpenGL.so*) continue ;;
        esac
        if [ ! -e "release/game/$name" ]; then
            cp -L "$library" "release/game/$name"
        fi
    done < <(LD_LIBRARY_PATH="$(pwd)/release/game" ldd "$binary" 2>/dev/null)
done < <(find release/game -type f \( -name '*.so*' -o -name 'launch' -o -name 'astrond-linux' \) -print0)

# Fail packaging if the game, plugins, or Astron have unresolved dependencies.
while IFS= read -r -d '' binary; do
    dependencies=$(LD_LIBRARY_PATH="$(pwd)/release/game" ldd "$binary" 2>&1) || { echo "$dependencies" >&2; exit 1; }
    if [[ "$dependencies" == *"not found"* ]]; then
        echo "Unresolved runtime dependencies for $binary: $dependencies" >&2
        exit 1
    fi
done < <(find release/game -type f \( -name '*.so*' -o -name 'launch' -o -name 'astrond-linux' \) -print0)

echo "Compressing release into TTAP-linux.zip..."
rm -f TTAP-linux.zip
zip -r TTAP-linux.zip release

echo "=== Linux Build Complete: TTAP-linux.zip ==="
