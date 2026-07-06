cd $(dirname $0 )
echo Starting Astron
# check if on an arm mac if so then start server_astron_arm 
if [ "$(uname -m)" = "arm64" ]; then 
    ./start_server_astron_arm.command &
else
    ./start_server_astron.command &
fi
sleep 2
echo Starting UberDOG

./start_server_ud.command &
sleep 2
echo Starting AI
./start_server_ai.command