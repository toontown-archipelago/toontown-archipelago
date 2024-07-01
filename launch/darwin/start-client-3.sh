#!/bin/sh
echo "Toontown Archipelago: Client 3 Launcher"
echo
export PPYTHON_PATH=$(cat PPYTHON_PATH)
export SERVICE_TO_RUN=CLIENT
cd ../..

echo "Enter your name (default: player3): "
read -r loginToken
export TTOFF_LOGIN_TOKEN=${loginToken:="player3"}

echo "Server IP (default: 127.0.0.1): "
read -r gameServer
export TTOFF_GAME_SERVER=${gameServer:="127.0.0.1"}

while true
do
	$PPYTHON_PATH -m pip install -r requirements.txt
	$PPYTHON_PATH -m launch.launcher.launch
	sleep 5
done