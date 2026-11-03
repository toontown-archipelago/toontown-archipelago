#!/usr/bin/env bash
echo "Toontown Archipelago: Astron Launcher"
echo

cd "$(dirname "$0")"
cd ../../astron

if [ "$(uname -m)" = "aarch64" ] || [ "$(uname -m)" = "arm64" ]; then
    ./astrond-linux-arm64 --loglevel info config/astrond.yml
else
    ./astrond-linux --loglevel info config/astrond.yml
fi
