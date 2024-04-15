@echo off
title Toontown Archipelago - Server Launcher

echo Starting Astron
start start_server_astron.bat

TIMEOUT /T 2
echo Starting UberDOG
start start_server_ud.bat

TIMEOUT /T 2
echo Starting AI
start start_server_ai.bat
