@echo off
title Toontown Archipelago: AI Launcher
set /P PPYTHON_PATH=<PPYTHON_PATH
set SERVICE_TO_RUN=AI
cd ..\..

set BASE_CHANNEL=401000000
set MAX_CHANNELS=999999
set STATE_SERVER=4002
set DISTRICT_NAME=Archipelago Avenue
set ASTRON_IP=127.0.0.1:7199
set EVENT_LOGGER_IP=127.0.0.1:7197

:main
    %PPYTHON_PATH% -m pip install -r requirements.txt
    %PPYTHON_PATH% -m launch.launcher.launch
    pause
goto main
