#!/usr/bin/env bash
cd "$(dirname "$0")"

pidFile="$(pwd)/.server_launcher.pid"
echo $$ > "$pidFile"
trap 'exit 0' INT TERM
trap 'rm -f "$pidFile"' EXIT

echo "Starting Astron..."
./start_server_astron.sh &

sleep 2

echo "Starting UberDOG..."
./start_server_ud.sh &

sleep 2

echo "Starting AI..."
./start_server_ai.sh &
wait $!
