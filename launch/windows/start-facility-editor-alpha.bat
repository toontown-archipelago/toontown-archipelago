@echo off
title Toontown Archipelago: Facility Editor [ALPHA]
set /P PPYTHON_PATH=<PPYTHON_PATH
set SERVICE_TO_RUN=CLIENT
cd ..\..

:main
    %PPYTHON_PATH% -m pip install -r requirements.txt
    %PPYTHON_PATH% -m toontown.toonbase.facility_room_builder
    pause
goto :main