#!/bin/bash


echo "Startar loop the Sleeper"

# Loopa för evigt
while true; do
    # Skriver ut innehållet i filen till terminalen
    cat /tmp/theBatt.txt

    m5_Before=$(md5sum "/tmp/theBatt.txt")
    echo "md5sum = $m5_Before-----------------------------"
    timeout -k 10s 1m python /home/pi/repo/SmartPlugTools/Python3/theSleeper.py
    echo "md5sum = $m5_After-----------------------------"
    
    m5_After=$(md5sum "/tmp/theBatt.txt")

    if [ "$m5_Before" == "$m5_After" ] ; then
        echo "REBOOT-----------------------------" >> /tmp/theBatt.txt
        sleep 120
        sudo reboot
    else
        echo "Keep running-----------------------------"
    fi

    # Vänta 1200 sekunder (så att scriptet inte äter upp all CPU)
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Will sleep 300 seconds: $0" >> /tmp/theBatt.txt
    sleep 1200
done
