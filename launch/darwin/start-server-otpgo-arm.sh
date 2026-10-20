#!/bin/sh
echo "Toontown Archipelago: OtpGo Launcher"
echo
cd "$(dirname "$0")/../.." || exit 1
mkdir -p otpgo/logs || exit 1

exec ./otpgo/otpgo-arm --loglevel info otpgo/otp.yml
