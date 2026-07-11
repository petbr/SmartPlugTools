#!/bin/bash


echo "Startar loop the Sleeper"
#cp /home/pi/theBatt.txt /tmp/theBatt.txt

if [ -f /home/pi/persFile.txt ] ; then
    cp /home/pi/persFile.txt /tmp/persFile.txt
    echo "-----------------" >> /home/pi/LogFile.txt
    date >> /home/pi/LogFile.txt
    echo "just cp'ed /home/pi/persfile.txt to /tmp/" >> /home/pi/LogFile.txt
    ls -al /tmp/persFile.txt  >> /home/pi/LogFile.txt
fi

vanta_eller_avbryt() {
    local total_tid=1200
    local raknare=0

    echo "Väntar i $total_tid sekunder... (Ta bort eller avbryt med /tmp/REBOOT)"

    while [ $raknare -lt $total_tid ]; do
        # Kontrollera om filen existerar
        if [ -f "/tmp/REBOOT" ]; then
            echo "Avbryter: Hittade /tmp/REBOOT!"
            return 0
        fi

        sleep 1
        ((raknare++))
    done

    echo "Tiden har löpt ut ($total_tid sekunder)."
}

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
        cp /tmp/persFile.txt /home/pi/persFile.txt
        sudo reboot
    else
        echo "Keep running, first TRIM the file-----------------------------"
        tail -n 1000 /tmp/theBatt.txt > /tmp/theBatt.tmp && mv /tmp/theBatt.tmp /tmp/theBatt.txt
        # Vänta 1200 sekunder (så att scriptet inte äter upp all CPU)
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Will sleep 1200 seconds: $0" >> /tmp/theBatt.txt
    fi
        
    if vanta_eller_avbryt; then
        echo "Avbrott eller klar. Startar om nu!"
        rm -f /tmp/REBOOT
    fi        

done
