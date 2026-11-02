#!/usr/bin/env bash
cd "$(dirname "$0")"

pidFile="$(pwd)/.server_astron.pid"
serverPid=
echo $$ > "$pidFile"
trap 'exit 0' INT TERM
trap 'kill "$serverPid" 2>/dev/null; wait "$serverPid" 2>/dev/null; rm -f "$pidFile"' EXIT

cd game/astron

while true;
do
    ./astrond --loglevel info config/astrond.yml &
    serverPid=$!
    wait "$serverPid"
    serverPid=
    sleep 5 
done
