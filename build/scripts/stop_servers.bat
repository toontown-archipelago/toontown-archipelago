@echo off
title Toontown Archipelago - Stop Servers

echo Stopping Server Launcher
taskkill /F /T /FI "WINDOWTITLE eq *Toontown Archipelago - Server Launcher*" /IM cmd.exe 2>nul

echo Stopping AI
taskkill /F /T /FI "WINDOWTITLE eq *Toontown Archipelago - AI (District) Server*" /IM cmd.exe 2>nul

echo Stopping UberDOG
taskkill /F /T /FI "WINDOWTITLE eq *Toontown Archipelago - UberDOG Server*" /IM cmd.exe 2>nul

echo Stopping Astron
taskkill /F /T /FI "WINDOWTITLE eq *Toontown Archipelago - Astron Server*" /IM cmd.exe 2>nul

exit /B 0
