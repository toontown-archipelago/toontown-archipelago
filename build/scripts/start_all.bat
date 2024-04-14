@echo off
title Toontown Archipelago - UberDOG Server

echo Starting Astron
start start_astron.bat

TIMEOUT /T 2
echo Starting UberDOG
start start_server_ud.bat

TIMEOUT /T 2
echo Starting AI
start start_server_ai.bat

TIMEOUT /T 2
echo Starting Client
start start_client.bat