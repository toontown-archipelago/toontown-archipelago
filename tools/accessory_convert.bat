@echo off
set /P PPYTHON_PATH=<PPYTHON_PATH

cd ../

%PPYTHON_PATH% -m accessoryplacer.MigrateGlobals
echo Accessory conversion completed, have a nice day
@echo off
@timeout /t 5 > nul