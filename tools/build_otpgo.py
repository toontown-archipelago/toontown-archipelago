import argparse
import hashlib
import os
from pathlib import Path
import platform
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
REVISION = '3bd67275c6677b1f28b535771e8665bb6d380b91'
REPOSITORY = 'https://github.com/LittleToonCat/OtpGo.git'
TARGETS = {
    'darwin/amd64': 'otpgo',
    'darwin/arm64': 'otpgo-arm',
    'linux/amd64': 'otpgo-linux',
    'linux/arm64': 'otpgo-linux-arm64',
    'windows/amd64': 'otpgo.exe',
}


def main():
    parser = argparse.ArgumentParser(description='Build pinned OtpGo binaries with the TTAP patches')
    parser.add_argument('--all', action='store_true', help='Build every supported platform')
    parser.add_argument('--target', choices=TARGETS, help='Build one platform')
    args = parser.parse_args()
    if args.all and args.target:
        parser.error('Choose either --all or --target')
    machine = 'arm64' if platform.machine().lower() in ('arm64', 'aarch64') else 'amd64'
    host = platform.system().lower() + '/' + machine
    targets = list(TARGETS) if args.all else [args.target or host]
    if any(target not in TARGETS for target in targets):
        parser.error('Unsupported host platform; specify --target')
    with tempfile.TemporaryDirectory(prefix='ttap-otpgo-') as directory:
        source = Path(directory) / 'source'
        subprocess.run(['git', 'init', str(source)], check=True)
        subprocess.run(['git', 'remote', 'add', 'origin', REPOSITORY], cwd=source, check=True)
        subprocess.run(['git', 'fetch', '--depth', '1', 'origin', REVISION], cwd=source, check=True)
        subprocess.run(['git', 'checkout', '--detach', REVISION], cwd=source, check=True)
        subprocess.run(['git', 'apply', str(ROOT / 'otpgo/patches/ttap.patch')], cwd=source, check=True)
        for target in targets:
            output = ROOT / 'otpgo' / TARGETS[target]
            goos, goarch = target.split('/')
            env = dict(os.environ, GOOS=goos, GOARCH=goarch, CGO_ENABLED='0')
            subprocess.run([
                'go', 'build', '-trimpath', '-tags', 'no_mongodb,no_mysql,no_postgres',
                '-o', str(output), '.'
            ], cwd=source, env=env, check=True)
            print('Built %s' % output, flush=True)
    files = [ROOT / 'otpgo' / name for name in TARGETS.values()]
    checksums = [hashlib.sha256(file.read_bytes()).hexdigest() + '  ' + file.name
                 for file in files if file.is_file()]
    (ROOT / 'otpgo/SHA256SUMS').write_text('\n'.join(checksums) + '\n')


if __name__ == '__main__':
    main()
