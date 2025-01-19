#!/bin/sh
echo "Toontown Ranked: Astron Launcher"
echo
cd ../../astron

./astrond-arm --loglevel info config/astrond.yml
