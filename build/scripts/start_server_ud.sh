#!/usr/bin/env bash
cd "$(dirname "$0")"

export SERVICE_TO_RUN=UD
cd game

export LD_LIBRARY_PATH="$(pwd):${LD_LIBRARY_PATH:-}"
export BASE_CHANNEL=1000000
export MAX_CHANNELS=999999
export STATESERVER=4002
export ASTRON_IP="127.0.0.1:7199"
export EVENTLOGGER_IP="127.0.0.1:7197"

while true; do
    ./launch \
        config/common.prc \
        config/production.prc
    sleep 5
done
