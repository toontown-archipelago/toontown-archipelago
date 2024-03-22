@echo off
title Toontown Archipelago - Game Client
cd..

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

set TTOFF_LOGIN_TOKEN=dev

set /P ARCHIPELAGO_SLOT="(Archipelago) Slot Name: " || ^
set ARCHIPELAGO_SLOT=Colorful Toon

set /P ARCHIPELAGO_ADDRESS="(Archipelago) Server Address: " || ^
set ARCHIPELAGO_ADDRESS=localhost:38281

:launcher
%PPYTHON_PATH% -m toontown.launcher.TTOffQuickStartLauncher
pause
goto :launcher
