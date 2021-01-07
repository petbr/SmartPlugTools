#!/bin/bash
# This runs in Crontab to check that the wifi is working.  If it is faulty it will 
# firstly restart wifi and check all is running well.  If not, the script will reboot the PI
# Any checks and reboots are stored as actions in txt files in /home/pi/DomCode
# Dominic 29/1/2020

while :
do

# Lines below are to get the date and time variables ready
BASHDATE=`date +"%b %d, %Y"`
BASHTIME=`date +" %T"`
# Start of code
ping -c1 192.168.1.1 > /dev/null
if [ $? != 0 ] 
then
#	WiFi is down so going into the next phase of this file to check, reset and reboot too if necessary
#	echo WiFi all bad, restarting it on ${BASHDATE} at: ${BASHTIME} >> /home/pi/DomCode/WiFi_bad.txt
	echo WiFi all bad, restarting it on ${BASHDATE} at: ${BASHTIME}
	sudo ifconfig wlan0 down
	sleep 5
#	Restarting WIFI if needed
	sudo ifconfig wlan0 up
	sleep 18
	sleep 2
#	Re-pinging after wifi re-start	
	ping -c1 10.3.1.1 > /dev/null
#	If Ping fails the PI will restart
	if [ $? != 0 ]
	then
#		echo WiFi all bad, restarting the PI on ${BASHDATE} at: ${BASHTIME} >> /home/pi/DomCode/WiFi_bad_reboot.txt
		echo WiFi all bad, restarting the PI on ${BASHDATE} at: ${BASHTIME}
		sleep 5
		echo sudo reboot will NOT happen!!!!
        else
		echo WiFi good after restarting it on ${BASHDATE} at: ${BASHTIME}
	fi

else
# If all is good this is written to a text file.  I'll reduce this to only having one line kept becuase later
#	echo WiFi all good on ${BASHDATE} at:  ${BASHTIME} > /home/pi/DomCode/WiFi_good.txt
	echo WiFi all good on ${BASHDATE} at:  ${BASHTIME}
fi

sleep 20
done