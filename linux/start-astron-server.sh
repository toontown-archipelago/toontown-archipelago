#!/bin/sh
cd astron/linux || { echo "Could not find the astron/linux directory!"; exit 1; }

# This assumes that your astrond build is located in the
# "astron/linux" directory.
./astrond --loglevel info ../config/astrond.yml