#!/bin/sh
echo "Toontown Archipelago: Astron Launcher"
echo
cd ../../astron

./astrond-linux --loglevel info config/astrond.yml
