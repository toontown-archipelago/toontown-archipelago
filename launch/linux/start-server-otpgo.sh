#!/bin/sh
echo "Toontown Archipelago: OtpGo Launcher"
echo
cd "$(dirname "$0")/../.." || exit 1
mkdir -p otpgo/logs || exit 1

case "$(uname -m)" in
    aarch64|arm64)
        exec ./otpgo/otpgo-linux-arm64 --loglevel info otpgo/otp.yml
        ;;
    *)
        exec ./otpgo/otpgo-linux --loglevel info otpgo/otp.yml
        ;;
esac
