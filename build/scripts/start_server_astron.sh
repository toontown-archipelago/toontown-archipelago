#!/usr/bin/env bash
cd "$(dirname "$0")"

pidFile="$(pwd)/.server_astron.pid"
serverPid=
echo $$ > "$pidFile"
trap 'exit 0' INT TERM
trap 'kill "$serverPid" 2>/dev/null; wait "$serverPid" 2>/dev/null; rm -f "$pidFile"' EXIT

cd game/astron

while true; do
    if [ "$(uname -m)" = "aarch64" ] || [ "$(uname -m)" = "arm64" ]; then
        ./astrond-linux-arm64 --loglevel info config/astrond.yml &
    else
        ./astrond-linux --loglevel info config/astrond.yml &
    fi
    serverPid=$!
    wait "$serverPid"
    serverPid=
    sleep 5
done
