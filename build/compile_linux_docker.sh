#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."

echo "=== Building Linux Release via Docker ==="

if ! command -v docker &> /dev/null; then
    echo "Error: docker command not found. Please ensure Docker is running."
    exit 1
fi

IMAGE_NAME="ttap-linux-builder"
CONTAINER_NAME="ttap-linux-build-run"

PLATFORM_ARG=""
if [ "$(uname -m)" = "arm64" ]; then
    echo "Detected Apple Silicon (arm64). Building for linux/amd64 (x86_64)..."
    PLATFORM_ARG="--platform linux/amd64"
fi

echo "Building Docker build image (compiles Panda3D from source with OpenAL & OpenGL)..."
docker build $PLATFORM_ARG -f launch/docker/build-linux.dockerfile -t "$IMAGE_NAME" .

echo "Running build container to assemble game release..."
docker rm -f "$CONTAINER_NAME" 2>/dev/null || true
docker run $PLATFORM_ARG --name "$CONTAINER_NAME" "$IMAGE_NAME"

echo "Extracting release artifacts to host..."
docker cp "$CONTAINER_NAME:/app/TTAP-linux.zip" ./TTAP-linux.zip
mkdir -p ./dist
docker cp "$CONTAINER_NAME:/dist/." ./dist/ 2>/dev/null || true
docker rm -f "$CONTAINER_NAME"

echo "=== Build Complete! ==="
echo "Game Release: ./TTAP-linux.zip"
echo "Panda3D Wheel: ./dist/"
