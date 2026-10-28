#!/usr/bin/env bash
cd "$(dirname "$0")"
cd game/astron

while true; do
    if [ "$(uname -m)" = "aarch64" ] || [ "$(uname -m)" = "arm64" ]; then
        ./astrond-linux-arm64 --loglevel info config/astrond.yml
    else
        ./astrond-linux --loglevel info config/astrond.yml
    fi
    sleep 5
done
