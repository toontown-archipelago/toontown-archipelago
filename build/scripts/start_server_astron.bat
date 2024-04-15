@echo off
title Toontown Archipelago - Astron Server
cd game\astron

:launch
astrond --loglevel info config/astrond.yml
pause
goto :launch
