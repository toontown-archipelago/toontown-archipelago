@echo off
title Toontown Archipelago - Astron Server
cd ../astron
astrond --loglevel info config/astrond.yml
pause
