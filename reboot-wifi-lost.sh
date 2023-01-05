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
ping_delay=20
ping_repeat=5

echo #2

echo ---------- Reboot surveillance >> /var/log/DranpumpData/TheThing.log
echo ---------- Wait five minutes until GO! >> /var/log/DranpumpData/TheThing.log
date >> /var/log/DranpumpData/TheThing.log

echo #3

sleep 300

echo #4

echo >> /var/log/DranpumpData/TheThing.log
echo >> /var/log/DranpumpData/TheThing.log
echo ---------- Reboot surveillance NOW Starts>> /var/log/DranpumpData/TheThing.log
date >> /var/log/DranpumpData/TheThing.log
echo ----------- NOW.....Start Reboot surveillance!!! >> /var/log/DranpumpData/TheThing.log
echo >> /var/log/DranpumpData/TheThing.log

# ping the target the desired number of times. If 'ping' is successful,
# the 'let count="0"' executres, returns a non zero exit code and the 
# script exits due to 'set -e'. If all 'ping' operations fail, the host
# reboots.
while [ $count -lt "$ping_repeat" ] ; do

    sleep "$ping_delay"
    # shellcheck disable=SC2015 # SC2015 is intended logic
    ping -c1 "$1" &> /dev/null && (( count="0" )) || (( count="$count + 1" ))

    if  [ -f /var/log/DranpumpData/REBOOT ]
    then
        count=1000
        echo ---------- Fake no internet with REBOOT touched file >> /var/log/DranpumpData/TheThing.log
    fi

done


echo ---------- The shit is not ping responding EXIT in five minutes after copying log file >> /var/log/DranpumpData/TheThing.log
date >> /var/log/DranpumpData/TheThing.log

echo ---------- Reboot drainpump plug  >> /var/log/DranpumpData/TheThing.log
cp /var/log/DranpumpData/TheThing.log /home/pi/TheThing.log

/usr/bin/python3.5 /home/pi/repo/SmartPlugTools/Python3/restartDevice_UsingClass.py 
echo ---------- Reboot drainpump plug DONE!  >> /var/log/DranpumpData/TheThing.log
cp /var/log/DranpumpData/TheThing.log /home/pi/TheThing.log

echo ----------- Let us reboot >> /var/log/DranpumpData/TheThing.log
cp /var/log/DranpumpData/TheThing.log /home/pi/TheThing.log

sleep 300

#reboot
sudo reboot
