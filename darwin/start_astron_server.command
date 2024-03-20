#!/bin/sh
cd ..
cd astron || { echo "Could not find the astron directory!"; exit 1; }

./astrond-darwin --loglevel info config/astrond.yml
