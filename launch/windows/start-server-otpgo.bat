@echo off
title Toontown Archipelago: OtpGo Launcher
cd /d "%~dp0..\.."
if errorlevel 1 exit /b 1
if not exist otpgo\logs mkdir otpgo\logs
if errorlevel 1 exit /b 1

:main
    otpgo\otpgo.exe --loglevel info otpgo/otp.yml
    pause
goto main
