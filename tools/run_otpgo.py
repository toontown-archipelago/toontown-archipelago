import argparse
import os
from pathlib import Path
import platform
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description='Run the local OtpGo development stack')
    parser.add_argument('service', choices=['server', 'ai', 'ud', 'client'])
    parser.add_argument('--token', default='player1')
    args = parser.parse_args()
    os.chdir(ROOT)
    for directory in ('databases', 'logs', 'backups'):
        (ROOT / 'otpgo' / directory).mkdir(exist_ok=True)
    if args.service == 'server':
        from build_otpgo import TARGETS
        machine = 'arm64' if platform.machine().lower() in ('arm64', 'aarch64') else 'amd64'
        target = platform.system().lower() + '/' + machine
        if target not in TARGETS:
            parser.error('Unsupported server platform: %s' % target)
        binary = ROOT / 'otpgo' / TARGETS[target]
        if not binary.is_file():
            parser.error('Build OtpGo first: python tools/build_otpgo.py')
        return subprocess.call([str(binary), '--loglevel', 'info', 'otpgo/otp.yml'])

    from panda3d.core import loadPrcFile
    for prc in ('common', 'development', 'otpgo'):
        loadPrcFile(str(ROOT / 'config' / (prc + '.prc')))
    sys.path.insert(0, str(ROOT))
    if args.service == 'client':
        os.environ['TTOFF_LOGIN_TOKEN'] = args.token
        os.environ['TTOFF_GAME_SERVER'] = '127.0.0.1'
        from toontown.launcher import TTOffQuickStartLauncher
    else:
        os.environ['BASE_CHANNEL'] = '401000000' if args.service == 'ai' else '1000000'
        os.environ['MAX_CHANNELS'] = '999999'
        os.environ['STATESERVER'] = '4002'
        os.environ['ASTRON_IP'] = '127.0.0.1:7199'
        os.environ['DISTRICT_NAME'] = 'Archipelago Avenue'
        sys.argv = [sys.argv[0], 'config/common.prc', 'config/development.prc', 'config/otpgo.prc']
        if args.service == 'ai':
            from toontown.ai import AIStart
        else:
            from toontown.uberdog import UDStart


if __name__ == '__main__':
    sys.exit(main())
