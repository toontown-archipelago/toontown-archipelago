#!/bin/sh
echo "Toontown Archipelago: Astron Launcher"
echo
cd ../../astron

./astrond-arm --loglevel info config/astrond.yml
