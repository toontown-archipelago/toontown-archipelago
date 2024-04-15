@echo off
title Toontown Archipelago: Astron Launcher
cd ..\..\astron

:main
    astrond.exe --loglevel info config/astrond.yml
    pause
goto main
