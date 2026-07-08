#!/bin/bash


echo "Startar loop the Sleeper"
#cp /home/pi/theBatt.txt /tmp/theBatt.txt

# Loopa för evigt
while true; do
    # Skriver ut innehållet i filen till terminalen
    cat /tmp/theBatt.txt

    m5_Before=$(md5sum "/tmp/theBatt.txt")
    echo "md5sum = $m5_Before-----------------------------"
    timeout -k 10s 1m python /home/pi/repo/SmartPlugTools/Python3/theSleeper.py
    echo "md5sum = $m5_After-----------------------------"
    
    m5_After=$(md5sum "/tmp/theBatt.txt")

    # If nothing happened....measurement has failed
    if [ "$m5_Before" == "$m5_After" ] || [ -f /tmp/REBOOT ] ; then
        echo "REBOOT-----------------------------" >> /tmp/theBatt.txt
        sleep 120
        #cat /tmp/theBatt.txt  >> /home/pi/theBatt.txt
        sudo reboot
    else
        echo "Keep running, first TRIM the file-----------------------------"
        tail -n 1000 /tmp/theBatt.txt > /tmp/theBatt.tmp && mv /tmp/theBatt.tmp /tmp/theBatt.txt
        # Vänta 1200 sekunder (så att scriptet inte äter upp all CPU)
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Will sleep 1200 seconds: $0" >> /tmp/theBatt.txt
        sleep 1200        
    fi

done
