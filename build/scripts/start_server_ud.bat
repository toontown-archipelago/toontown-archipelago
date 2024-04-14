@echo off
title Toontown Archipelago - UberDOG Server
set SERVICE_TO_RUN=UD
cd game

:launch
start /B "%~dp0" "launch.exe" ^
    --base-channel 1000000 ^
    --max-channels 999999 ^
    --stateserver 4002 ^
    --astron-ip 127.0.0.1:7199 ^
    --eventlogger-ip 127.0.0.1:7197 ^
    config/common.prc ^
    config/production.prc
pause
goto :launch
