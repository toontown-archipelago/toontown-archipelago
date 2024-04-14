@echo off
title Toontown Archipelago - Launcher

echo Starting Astron
start start_servers.bat

TIMEOUT /T 2
echo Starting Client
start start_client.bat