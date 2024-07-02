
export SERVICE_TO_RUN=AI
cd game
export BASE_CHANNEL=401000000
export MAX_CHANNELS=999999
export STATESERVER=4002
export ASTRON_IP="127.0.0.1:7199"
export EVENTLOGGER_IP="127.0.0.1:7197"
export DISTRICT_NAME="Archipelago Avenue"
while true;
do
    ./launch \
    config/common.prc \
    config/production.prc
    sleep 5
done