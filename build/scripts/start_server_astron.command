cd $(dirname $0 )
cd game/astron

while true;
do
    ./astrond --loglevel info config/astrond.yml
    sleep 5 
done