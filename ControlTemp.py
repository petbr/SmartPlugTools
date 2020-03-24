#!/usr/bin/env python3

import os 
import subprocess
import time

def getFanSpeedAndTemp1():
	sensors = subprocess.Popen(['sensors'], 
				stdout=subprocess.PIPE, 
				stderr=subprocess.STDOUT,
				encoding='utf8')

	stdout, stderr = sensors.communicate()

	i = 0
	stdoutArray = stdout.split('\n')
	for line in stdoutArray:
		if len(line) == 0:
			line = 'EMPTY'
		lineArray = line.split()
		if line == 'acpitz-virtual-0':
			lineArray = stdoutArray[i+2].split()
			temp1 = float(lineArray[1][:-2])
		if lineArray[0] == 'fan1:':
			fanSpeed = float(lineArray[1])
		i = i+1

	return (fanSpeed, temp1)

oldSpeed = -1
def setFanSpeed(speed):
	global oldSpeed
	if oldSpeed != speed:
		cmd = 'echo level ' + str(speed) + '  > /proc/acpi/ibm/fan'
		print("Set speed = ", speed)
		os.system(cmd)
		oldSpeed = speed
		
while True:
	(fanSpeed, temp1) = getFanSpeedAndTemp1()
	print("fanspeed = ", fanSpeed, ", temp1 = ", temp1)
	
	if temp1 > 52:
		setFanSpeed(7)
	elif temp1 > 50:
		setFanSpeed(6)
	elif temp1 > 48:
		setFanSpeed(5)
	elif temp1 > 46:
		setFanSpeed(4)
	elif temp1 > 44:
		setFanSpeed(3)
	elif temp1 > 42:
		setFanSpeed(2)
	else:
		setFanSpeed(1)

	time.sleep(5)	

#acpitz-virtual-0
#Adapter: Virtual device
#temp1:        +35.0°C  (crit = +200.0°C)
