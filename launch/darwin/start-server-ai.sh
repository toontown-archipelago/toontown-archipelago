#!/bin/sh
echo "Toontown Archipelago: AI Launcher"
echo
export PPYTHON_PATH=$(cat PPYTHON_PATH)
export SERVICE_TO_RUN=AI
cd ../..

export BASE_CHANNEL=401000000
export MAX_CHANNELS=999999
export STATESERVER=4002
export ASTRON_IP="127.0.0.1:7199"
export EVENTLOGGER_IP="127.0.0.1:7197"
export DISTRICT_NAME="Archipelago Avenue"
export WANT_ERROR_REPORTING="true"

while true
do
	$PPYTHON_PATH -m pip install -r requirements.txt
	$PPYTHON_PATH -m launch.launcher.launch
	sleep 5
done
