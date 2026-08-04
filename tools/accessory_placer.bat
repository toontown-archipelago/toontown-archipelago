set /P PPYTHON_PATH=<PPYTHON_PATH

cd ../
:e
%PPYTHON_PATH% -m accessoryplacer.AccessoryPlacer

pause
goto e