#!/bin/sh
cd ..

export TTOFF_LOGIN_TOKEN="dev"

/usr/local/bin/python3.9 -m toontown.launcher.TTOffQuickStartLauncher
