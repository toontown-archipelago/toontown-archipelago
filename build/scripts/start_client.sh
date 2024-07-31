export SERVICE_TO_RUN=CLIENT
cd game
echo "Enter your name (default: player): "
read -r loginToken
export TTOFF_LOGIN_TOKEN=${loginToken:="player1"}
echo "Server IP (default: 127.0.0.1): "
read -r gameServer
export TTOFF_GAME_SERVER=${gameServer:="127.0.0.1"}

 # launch the unix executable
 ./launch 
sleep 5
