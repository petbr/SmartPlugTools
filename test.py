#!/usr/bin/env python2
#
# TP-Link Wi-Fi Smart Plug Protocol Client
# For use with TP-Link HS-100 or HS-110
#
# by Lubomir Stroetmann
# Copyright 2016 softScheck GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Usage in Stora Hoga:
# python tplink_smartplug.py -t 192.168.1.18 -c energy

import socket
import time
import enum
import argparse
from struct import pack

version = 0.2

# Predefined Smart Plug Commands
# For a full list of commands, consult tplink_commands.txt
commands = {'info'     : '{"system":{"get_sysinfo":{}}}',
            'on'       : '{"system":{"set_relay_state":{"state":1}}}',
            'off'      : '{"system":{"set_relay_state":{"state":0}}}',
            'cloudinfo': '{"cnCloud":{"get_info":{}}}',
            'wlanscan' : '{"netif":{"get_scaninfo":{"refresh":0}}}',
            'time'     : '{"time":{"get_time":{}}}',
            'schedule' : '{"schedule":{"get_rules":{}}}',
            'countdown': '{"count_down":{"get_rules":{}}}',
            'antitheft': '{"anti_theft":{"get_rules":{}}}',
            'reboot'   : '{"system":{"reboot":{"delay":1}}}',
            'reset'    : '{"system":{"reset":{"delay":1}}}',
            'energy'   : '{"emeter":{"get_realtime":{}}}'}

port = 9999
timeCmd    = commands["time"]
powerCmd   = commands["energy"]
turnOnCmd  = commands["on"]
turnOffCmd = commands["off"]

class PowerDirection(enum.Enum): 
    powerStable      = 1
    powerIncreasingt = 2
    powerDecreasing  = 3

class PumpMode(enum.Enum): 
    idle_short    = 1
    idle_long     = 2
    pumpingAir    = 3
    pumpTurnedOff = 4
    pumpingWater  = 5
    
# Check if hostname is valid
def validHostname(hostname):
	try:
		socket.gethostbyname(hostname)
	except socket.error:
		parser.error("Invalid hostname.")
	return hostname

# Encryption and Decryption of TP-Link Smart Home Protocol
# XOR Autokey Cipher with starting key = 171
def encrypt(string):
	key = 171
	result = pack('>I', len(string))
	for i in string:
		a = key ^ ord(i)
		key = a
		result += chr(a)
	return result

def decrypt(string):
	key = 171
	result = ""
	for i in string:
		a = key ^ ord(i)
		key = ord(i)
		result += chr(a)

	return result

# Ex.     inData: "{"emeter":{"get_realtime":{"current":0.036836,"voltage":233.437091,"power":3.172235,"total":5.032000,"err_code":0}}}')"
#         field:  "power"                                                              1      ffffffffE
#                                                                                      ssssssssssssssssssssssssssssssssssssssssssssssssss
# Ex.     inData: "{"emeter":{"get_realtime":{"current":0.036836,"voltage":233.437091,"power":3.172235,"total":5.032000,"err_code":0}}}')"
#         field:  "err_code"                                                                                             1         fE
#                                                                                      ssssssssssssssssssssssssssssssssssssssssssssssssss
def findValueStr(inData, field):
	findPos = inData.find(field)                       #1
	findAndRest = inData[findPos:]                     #s
	nextValueEndPos = findAndRest.find(',')            #E
	if nextValueEndPos == -1:
		nextValueEndPos = findAndRest.find('}')        #E

	findValue = findAndRest[len(field)+2 : nextValueEndPos] #f

	return findValue

def sendAndReceiveOnSocket(ip, port, cmd):
	try:
		# Connect socket
		sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock_tcp.connect((ip, port))

		sock_tcp.send(encrypt(cmd))
		data = sock_tcp.recv(2048)

		#Close socket connection
		sock_tcp.close()

	except socket.error:
		quit("Cound not connect to host " + ip + ":" + str(port))

	return data

#python check_husqvarna.py -t 192.168.1.18 -c off
#('Sent:     ', '{"system":{"set_relay_state":{"state":0}}}')
#('Received: ', '{"system":{"set_relay_state":{"err_code":0}}}')
def setTurnOff(ip):
  turnOffResult = sendAndReceiveOnSocket(ip, port, turnOffCmd)
  decryptedTurnOffData = decrypt(turnOffResult[4:])
  
  turnOffRes = {'err_code' : int(findValueStr(decryptedTurnOffData, "err_code"))}
  
  print("TURN_OFF: E:{e:01d}"
      .format(e=turnOffRes["err_code"]))
  
  return turnOffRes

#python check_husqvarna.py -t 192.168.1.18 -c on
#('Sent:     ', '{"system":{"set_relay_state":{"state":1}}}')
#('Received: ', '{"system":{"set_relay_state":{"err_code":0}}}')
def setTurnOn(ip):
  turnOnResult = sendAndReceiveOnSocket(ip, port, turnOnCmd)
  decryptedTimeData = decrypt(turnOnResult[4:])
  
  turnOnRes = {'err_code' : int(findValueStr(decryptedTimeData, "err_code"))}
  
  print("TURN_ON: E:{e:01d}"
      .format(e=turnOnRes["err_code"]))
  
  return turnOnRes

#python check_husqvarna.py -t 192.168.1.18 -c time
#('Sent:     ', '{"time":{"get_time":{}}}')
#('Received: ', '{"time":{"get_time":{"err_code":0,"year":2019,"month":1,"mday":21,"wday":1,"hour":19,"min":33,"sec":47}}}')
def getDateTime(ip):
  #print("getTime, ip = ", ip)

  timeData   = sendAndReceiveOnSocket(ip, port, timeCmd)
  decryptedTimeData = decrypt(timeData[4:])
  #print("decryptedTimeData = ", decryptedTimeData)
  
  dateTime = {'year'     : int(findValueStr(decryptedTimeData,  "year")),
              'month'    : int(findValueStr(decryptedTimeData,  "month")),
              'mday'     : int(findValueStr(decryptedTimeData,  "mday")),
              'hour'     : int(findValueStr(decryptedTimeData,  "hour")),
              'min'      : int(findValueStr(decryptedTimeData,  "min")),
              'sec'      : int(findValueStr(decryptedTimeData,  "sec")),
              'err_code' : int(findValueStr(decryptedTimeData, "err_code"))}
  
  
  #print("TIME: {y:4d}-{m:02d}-{d:02d} {hr:02d}:{min:02d}:{sec:02d} E:{e:01d}"
      #.format(y=dateTime["year"],
              #m=dateTime["month"],
              #d=dateTime["mday"],
              #hr=dateTime["hour"],
              #min=dateTime["min"],
              #sec=dateTime["sec"],
              #e=dateTime["err_code"]))
  
  return dateTime

#python check_husqvarna.py -t 192.168.1.18 -c energy
#('Sent:     ', '{"emeter":{"get_realtime":{}}}')
#('Received: ', '{"emeter":{"get_realtime":{"current":0.012866,"voltage":234.916847,"power":0.333881,"total":1.291000,"err_code":0}}}')
def getPower(ip):
  #print("getPower, ip = ", ip)

  powerData = sendAndReceiveOnSocket(ip, port, powerCmd)
  decryptedPowerData = decrypt(powerData[4:])

  power = {'current'  : float(findValueStr(decryptedPowerData, "current")),
           'voltage'  : float(findValueStr(decryptedPowerData, "voltage")),
           'power'    : float(findValueStr(decryptedPowerData, "power")),
           'total'    : float(findValueStr(decryptedPowerData, "total")),
           'err_code' : int(findValueStr(decryptedPowerData, "err_code"))}
  
  #print("POWER: I={i:5.5f} U={u:5.2f} P={p:5.5f} T={t:5.6f} E:{e:01d}"
        #.format(i=power['current'],
                #u=power['voltage'],
                #p=power['power'],
                #t=power['total'],
                #e=power['err_code']))
  
  return power

def someRunExamples(ip):
  turnOff  = setTurnOff(ip)
  dateTimeAtOff = getDateTime(ip)
  powerAtOff    = getPower(ip)
  
  print("returned TURN_OFF: E:{e:01d}"
        .format(e=turnOff["err_code"]))
  print("returned TIME @ Off: {y:4d}-{m:02d}-{d:02d} {hr:02d}:{min:02d}:{sec:02d} E:{e:01d}"
        .format(y=dateTimeAtOff["year"],
                m=dateTimeAtOff["month"],
                d=dateTimeAtOff["mday"],
                hr=dateTimeAtOff["hour"],
                min=dateTimeAtOff["min"],
                sec=dateTimeAtOff["sec"],
                e=dateTimeAtOff["err_code"]))
  print("returned POWER @ Off: I={i:5.5f} U={u:5.2f} P={p:5.5f} E:{e:01d}\n\n"
        .format(i=powerAtOff['current'],
                u=powerAtOff['voltage'],
                p=powerAtOff['power'],
                e=powerAtOff["err_code"]))
              
  time.sleep(2)

  # Turn ON
  turnOn  = setTurnOn(ip)
  time.sleep(2)

  dateTimeAtOn = getDateTime(ip)
  powerAtOn    = getPower(ip)

  print("returned TURN_ON: E:{e:01d}"
        .format(e=turnOn["err_code"]))
  print("returned TIME @ Off: {y:4d}-{m:02d}-{d:02d} {hr:02d}:{min:02d}:{sec:02d} E:{e:01d}"
        .format(y=dateTimeAtOn["year"],
                m=dateTimeAtOn["month"],
                d=dateTimeAtOn["mday"],
                hr=dateTimeAtOn["hour"],
                min=dateTimeAtOn["min"],
                sec=dateTimeAtOn["sec"],
                e=dateTimeAtOn["err_code"]))
  print("returned POWER @ On: I={i:5.5f} U={u:5.2f} P={p:5.5f} E:{e:01d}"
        .format(i=powerAtOn['current'],
                u=powerAtOn['voltage'],
                p=powerAtOn['power'],
                e=powerAtOn["err_code"]))
  return

def printDateTime(dateTime):
  print("TIME {y:4d}-{m:02d}-{d:02d} {hr:02d}:{min:02d}:{sec:02d} E:{e:01d}"
        .format(y=dateTime["year"],
                m=dateTime["month"],
                d=dateTime["mday"],
                hr=dateTime["hour"],
                min=dateTime["min"],
                sec=dateTime["sec"],
                e=dateTime["err_code"]))
  return

def printPower(pwr):
  print("POWER I={i:5.5f} U={u:5.2f} P={p:5.5f} E:{e:01d}"
        .format(i=pwr['current'],
                u=pwr['voltage'],
                p=pwr['power'],
                e=pwr["err_code"]))
  return

def printPumpMode(pumpMode):
  print ("Pump mode = {pm:s}"
         .format(pm=pumpMode.name))
  return

def printStatus(directive, duration,
                dateTime, pwr, mode):

  printDateTime(dateTime)
  print ("Duration = {t:5.2f}"
         .format(t=duration))
  print ("Shortest idle short time          = {t}"
         .format(t=shortestIdleShortDuration))
  print ("Longest idle short time           = {t}"
         .format(t=longestIdleShortDuration))
  print ("Shortest idle long time          = {t}"
         .format(t=shortestIdleLongDuration))
  print ("Longest idle long time           = {t}"
         .format(t=longestIdleLongDuration))
  print ("Shortest time pumping water = {t}"
         .format(t=shortestPumpWaterDuration))
  print ("Longest time pumping water  = {t}"
         .format(t=longestPumpWaterDuration))
  print ("Shortest time pumping air   = {t}"
         .format(t=shortestPumpAirDuration))
  print ("Longest time pumping air    = {t}"
         .format(t=longestPumpAirDuration))
  print ("Counter short to pump = {c}"
         .format(c=C_shortIdleToPump))
  print ("Counter long to pump = {c}"
         .format(c=C_longIdleToPump))
  printPower(pwr)
  printPumpMode(mode)
  print(directive)
  return

# Parse commandline arguments
parser = argparse.ArgumentParser(description="TP-Link Wi-Fi Smart Plug Client v" + str(version))
parser.add_argument("-t", "--target", metavar="<hostname>", required=True, help="Target hostname or IP address", type=validHostname)

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-c", "--command", metavar="<command>", help="Preset command to send. Choices are: "+", ".join(commands), choices=commands)

group.add_argument("-j", "--json", metavar="<JSON string>", help="Full JSON string of command to send")

args = parser.parse_args()

# Set target IP, port and command to send
ip = args.target


#class PowerDirection(enum.Enum): 
    #powerStable      = 1
    #powerIncreasingt = 2
    #powerDecreasing  = 3

# Power tresholds
P_idleTreshold = 20
P_airPumpingTreshold = 250
P_waterPumpingTreshold = 350

# Time tresholds
T_pumpingAirBeforeTurnOff = 5
T_maxOffTime              = 60
T_shortIdleTime           = 20

# Counter
C_shortIdleToPump = 0
C_longIdleToPump  = 0
#class PumpMode(enum.Enum): 
    #idle          = 1
    #pumpingAir    = 2
    #pumpTurnedOff = 3
    #pumpingWater  = 4


# idle -> pumpingWater -> pumpingAir/idle -> idle

powerState  = PowerDirection.powerStable
pumpMode    = PumpMode.idle_short
contRunning = True
prevPower   = 0
shortestIdleShortDuration      = 1000000/3.0
longestIdleShortDuration       = 1/3.0
shortestIdleLongDuration      = 1000000/3.0
longestIdleLongDuration       = 1/3.0
shortestPumpWaterDuration = 1000000/3.0
longestPumpWaterDuration  = 1/3.0
shortestPumpAirDuration   = 1000000/3.0
longestPumpAirDuration    = 1/3.0
switchTime = time.time()
setTurnOn(ip)    
dateTime = getDateTime(ip)
power    = getPower(ip)
printStatus("Just started ====> Turn ON and Idle short!\n", 0,
            dateTime, power, pumpMode)

while contRunning:
  dateTime = getDateTime(ip)
  power    = getPower(ip)
  powerValue = power['power']
    
  if (pumpMode is PumpMode.idle_short):
    changeTime = time.time()
    duration = changeTime-switchTime
    if powerValue > P_idleTreshold:
      shortestIdleShortDuration = min(duration, shortestIdleShortDuration)
      longestIdleShortDuration  = max(duration, longestIdleShortDuration)
      switchTime = changeTime
      C_shortIdleToPump = C_shortIdleToPump +1
      printStatus("Idle short ===> Pumping water\n", duration,
                  dateTime, power, pumpMode)

      pumpMode = PumpMode.pumpingWater
    elif duration > T_shortIdleTime:
      printStatus("Short idle ===> Idle long\n", duration,
                  dateTime, power, pumpMode)
      pumpMode = PumpMode.idle_long
      
  elif (pumpMode is PumpMode.idle_long):
    changeTime = time.time()
    duration = changeTime-switchTime
    if powerValue > P_idleTreshold:
      shortestIdleLongDuration = min(duration, shortestIdleLongDuration)
      longestIdleLongDuration  = max(duration, longestIdleLongDuration)
      switchTime = changeTime
      C_longIdleToPump = C_longIdleToPump +1
      printStatus("Idle Long ===> Pumping water\n", duration,
                  dateTime, power, pumpMode)
      pumpMode = PumpMode.pumpingWater

      
  elif pumpMode is PumpMode.pumpingWater:
    #print ("Pumping water, P={p:5.5f}"
    #       .format(p=powerValue))
    if powerValue < P_airPumpingTreshold:
      changeTime = time.time()      
      duration = changeTime-switchTime
      shortestPumpWaterDuration = min(duration, shortestPumpWaterDuration)
      longestPumpWaterDuration = max(duration, longestPumpWaterDuration)
      switchTime = changeTime
      printStatus("Pumping water ===> Pumping air\n", duration,
                  dateTime, power, pumpMode)

      pumpMode = PumpMode.pumpingAir
    
  elif pumpMode is PumpMode.pumpingAir:
    #print ("Pumping air, P={p:5.5f}"
    #       .format(p=powerValue))
    timePumpingAir = time.time()-switchTime
    if powerValue < P_idleTreshold:
      changeTime = time.time()      
      duration = changeTime-switchTime
      shortestPumpAirDuration = min(duration, shortestPumpAirDuration)
      longestPumpAirDuration  = max(duration, longestPumpAirDuration)
      switchTime = changeTime
      printStatus("Pumping Air short time ===> Idle short\n", duration,
                  dateTime, power, pumpMode)

      pumpMode = PumpMode.idle_short

    elif timePumpingAir > T_pumpingAirBeforeTurnOff:
      changeTime = time.time()      
      duration = changeTime-switchTime
      shortestPumpAirDuration = min(duration, shortestPumpAirDuration)
      longestPumpAirDuration  = max(duration, longestPumpAirDuration)
      setTurnOff(ip)    
      switchTime = changeTime      
      printStatus("Pumping Air too long time ===> Turn OFF!!!!\n", duration,
                  dateTime, power, pumpMode)

      pumpMode = PumpMode.pumpTurnedOff
    
  elif pumpMode is PumpMode.pumpTurnedOff:
    #print ("Pump turned off, P={p:5.5f}"
    #       .format(p=powerValue))
    offDuration = time.time() - switchTime      
    if offDuration > T_maxOffTime:
      changeTime = time.time()      
      print ("Duration = {t:5.2f}"
             .format(t=offDuration))
      setTurnOn(ip)
      switchTime = changeTime
      printStatus("OFF max time reached ===> Turn ON + Idle short!!!!\n", offDuration,
                  dateTime, power, pumpMode)

      pumpMode = PumpMode.idle_short
    
  else:
    print ("Pump mode = UNKNOWN, go to Idle")
    changeTime = time.time()
    duration = changeTime-switchTime
    switchTime = changeTime
    setTurnOn(ip)
    printStatus("OFF max time reached ===> Turn ON + Idle!!!!\n", duration,
                dateTime, power, pumpMode)

    pumpMode = PumpMode.idle_short
      
  if (powerValue > P_idleTreshold):
    time.sleep(1)
  else:
    time.sleep(5)

  prevPower = powerValue

#print("{y:4d}-{m:02d}-{d:02d} {hr:02d}:{min:02d}:{sec:02d} {p:f}"
#      .format(y=date_year, m=date_month, d=date_mday,
#              hr=time_hour, min=time_min, sec=time_sec,
#              p=emeter_power))

