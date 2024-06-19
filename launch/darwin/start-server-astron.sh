#!/bin/sh
echo "Toontown Archipelago: Astron Launcher"
echo
cd ../../astron

./astrond --loglevel info config/astrond.yml
