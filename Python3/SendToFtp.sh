#!/bin/bash

# Kontrollera att båda argumenten (User och Password) finns
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Användning: $0 <User> <Password>"
    exit 1
fi

# Spara argumenten i variabler
USER=$1
PASS=$2

echo "Startar loop för användare: $USER"
echo "Password: $PASS"

# Loopa för evigt
while true; do
    # Skriver ut innehållet i filen till terminalen
    cat /tmp/theBatt.txt
    
    python /home/pi/repo/SmartPlugTools/SendFileToFtp.py   privat.bahnhof.se   $USER $PASS /tmp/ theBatt.txt
    # Vänta 60 sekunder (så att scriptet inte äter upp all CPU)
    sleep 600
done
