#!/bin/sh
cd ..

MAX_CHANNELS=999999
STATE_SERVER=4002
ASTRON_IP="127.0.0.1:7199"
EVENT_LOGGER_IP="127.0.0.1:7197"
BASE_CHANNEL=1000000

/usr/local/bin/python3.9 -m pip install -r requirements.txt

while true
do
    /usr/local/bin/python3.9 -m toontown.uberdog.UDStart --base-channel ${BASE_CHANNEL} \
               --max-channels ${MAX_CHANNELS} --stateserver ${STATE_SERVER} \
               --astron-ip ${ASTRON_IP} \
               --eventlogger-ip ${EVENT_LOGGER_IP}
    sleep 5
done

