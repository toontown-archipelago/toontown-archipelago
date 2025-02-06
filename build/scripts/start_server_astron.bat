@echo off
title Toontown Ranked - Astron Server
cd game\astron

:launch
astrond --loglevel info config/astrond.yml
pause
goto :launch
