#!/bin/sh
cd ..

export TTOFF_LOGIN_TOKEN="dev"

python3 -m toontown.launcher.TTOffQuickStartLauncher
