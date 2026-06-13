#!/bin/bash


echo "Startar loop the Sleeper"

# Loopa för evigt
while true; do
    # Skriver ut innehållet i filen till terminalen
    cat /tmp/theBatt.txt
    
    python /home/pi/repo/SmartPlugTools/Python3/theSleeper.py
    # Vänta 60 sekunder (så att scriptet inte äter upp all CPU)
    sleep 60
done
