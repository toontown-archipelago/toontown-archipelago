@echo off
title Toontown Ranked: Astron Launcher
cd ..\..\astron

:main
    astrond.exe --loglevel info config/astrond.yml
    pause
goto main
