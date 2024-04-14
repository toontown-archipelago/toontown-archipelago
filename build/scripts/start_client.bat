@echo off
title Toontown Archipelago - Client
set SERVICE_TO_RUN=CLIENT
cd game

set /P TTOFF_LOGIN_TOKEN="Enter your name (default: player): " || ^
set TTOFF_LOGIN_TOKEN=player

set /P TTOFF_GAME_SERVER="Server IP (default: 127.0.0.1): " || ^
set TTOFF_GAME_SERVER=127.0.0.1

:launch
start /B "%~dp0" "launch.exe"
pause
goto :launcher