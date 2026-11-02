#!/usr/bin/env bash
cd "$(dirname "$0")"

echo "Stopping Servers..."

for server in launcher ai ud astron; do
    pidFile=".server_$server.pid"
    if [ ! -f "$pidFile" ]; then
        continue
    fi

    serverPid=$(cat "$pidFile")
    case "$serverPid" in
        ''|*[!0-9]*) continue ;;
    esac

    script="start_server_$server"
    if [ "$server" = "launcher" ]; then
        script="start_servers"
    fi
    case "$(ps -p "$serverPid" -o command=)" in
        *"$script.sh"*|*"${script}_arm.sh"*)
            kill "$serverPid" 2>/dev/null
            while [ -f "$pidFile" ] && kill -0 "$serverPid" 2>/dev/null; do
                sleep 0.1
            done
            ;;
    esac
done
