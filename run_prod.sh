#!/usr/bin/env bash

export ENV=prod

python2 ./src/moon_call.py
python2 ./src/cmc.py

hour=$(date +%H)

if (( "$hour" % 6 == 0 ))
then
    echo "Running post info on the 6th hour."
    python2 ./src/post_info.py
fi