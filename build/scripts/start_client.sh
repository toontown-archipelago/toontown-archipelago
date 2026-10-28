#!/usr/bin/env bash
cd "$(dirname "$0")"

export SERVICE_TO_RUN=CLIENT
cd game

# Ensure the executable directory is in LD_LIBRARY_PATH so dynamic plugins (.so) load correctly
export LD_LIBRARY_PATH="$(pwd):${LD_LIBRARY_PATH:-}"

echo "Enter your name (default: player): "
read -r loginToken
export TTOFF_LOGIN_TOKEN=${loginToken:="player1"}

echo "Server IP (default: 127.0.0.1): "
read -r gameServer
export TTOFF_GAME_SERVER=${gameServer:="127.0.0.1"}

# Launch the Linux client executable
./launch
sleep 2
