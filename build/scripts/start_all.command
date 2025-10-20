cd $(dirname $0 )
echo Starting Servers
./start_servers.command &

sleep 2
echo Starting Client
./start_client.command