#!/bin/bash

# see https://github.com/HankB/reboot-wifi-lost/blob/main/README.md for
# installation and usage notes

set -e # exit on error
set -u # exit on unset variable

if [ "$*""" = "" ] ; then
    echo "Usage $0 IP"
    exit 1
fi

echo #1

count=0
ping_delay=2
ping_repeat=5

echo #2

echo ---------- Reboot surveillance >> /var/log/DranpumpData/TheThing.log
echo ---------- Wait five minutes until GO! >> /var/log/DranpumpData/TheThing.log
date >> /var/log/DranpumpData/TheThing.log

echo #3


echo #4

# ping the target the desired number of times. If 'ping' is successful,
# the 'let count="0"' executres, returns a non zero exit code and the 
# script exits due to 'set -e'. If all 'ping' operations fail, the host
# reboots.
while [ $count -lt "$ping_repeat" ] ; do
    echo $count
    count=($count + 1)
    echo $count
    sleep "$ping_delay"
done


echo ---------- The shit is not ping responding EXIT in five minutes after copying log file >> /var/log/DranpumpData/TheThing.log


sleep 4

#reboot 18
#sudo reboot
echo Fake reboot 18
