#!/bin/bash


count=0
count_never_happens=90000
check_delay=20

while [ $count -lt "$count_never_happens" ] ; do

    sleep "$check_delay"

    if  [ -f /var/log/DranpumpData/REBOOT_PLUG ]
    then
        count=1000
        echo ---------- Fake no internet with REBOOT touched file >> /var/log/DranpumpData/TheThing.log
    fi

done

echo ---------- The shit is not ping responding EXIT in five minutes after copying log file >> /var/log/DranpumpData/TheThing.log
date >> /var/log/DranpumpData/TheThing.log
echo ---------- Reboot drainpump plug NOT
#     python3.5 Pytthon3/restartDevice_UsingClass.py 
#     echo ---------- Reboot drainpump plug DONE!

echo ----------- Let us reboot >> /var/log/DranpumpData/TheThing.log


#     Make a probably existing service chance to do whatever, for example reboot 240V Plug
touch /var/log/DranpumpData/REBOOT_PLUG

cp /var/log/DranpumpData/TheThing.log /home/pi/TheThing.log

sleep 300

#reboot
sudo reboot
