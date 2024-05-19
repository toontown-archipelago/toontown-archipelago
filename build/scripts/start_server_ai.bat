@echo off
title Toontown Archipelago - AI (District) Server
set SERVICE_TO_RUN=AI
cd game

:launch
start /B "%~dp0" "launch.exe" ^
    --base-channel 401000000 ^
    --max-channels 999999 ^
    --stateserver 4002 ^
    --astron-ip 127.0.0.1:7199 ^
    --eventlogger-ip 127.0.0.1:7197 ^
    --district-name "Toon Valley" ^
    config/common.prc ^
    config/production.prc
pause
goto :launch
