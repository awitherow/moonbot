#!/usr/bin/env bash

ENV=prod python2 ./src/moon_call.py

if [ date+%H % 6 == 0]
then
    ENV=prod python2 ./src/post_info.py
fi