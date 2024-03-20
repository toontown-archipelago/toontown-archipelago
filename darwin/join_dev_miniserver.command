#!/bin/sh
cd ..

echo "Toontown Archipelago Developer Mini-Server Launcher"
echo

echo "Input username (default: dev): "
read -r ttoffLoginToken
echo "Input game server address (default: 127.0.0.1): "
read -r ttoffGameServer

export TTOFF_LOGIN_TOKEN=${ttoffLoginToken:="dev"}
export TTOFF_GAME_SERVER=${ttoffGameServer:="127.0.0.1"}

/usr/local/bin/python3.9 -m toontown.launcher.TTOffQuickStartLauncher
