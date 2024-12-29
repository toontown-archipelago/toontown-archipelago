#!/bin/sh
echo "Toontown Ranked: Astron Launcher"
echo
cd ../../astron
# if architecture is arm64
if [ "$(uname -m)" = "aarch64" ]; then
    ./astrond-linux-arm64 --loglevel info config/astrond.yml
else
    ./astrond-linux --loglevel info config/astrond.yml
fi


