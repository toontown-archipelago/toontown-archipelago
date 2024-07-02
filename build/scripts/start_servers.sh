echo Starting Astron
# check if on an arm mac if so then start server_astron_arm 
if [ "$(uname -m)" = "arm64" ]; then 
    ./start_server_astron_arm.sh &
else
    ./start_server_astron.sh &
fi
sleep 2
echo Starting UberDOG

./start_server_ud.sh &
sleep 2
echo Starting AI
./start_server_ai.sh