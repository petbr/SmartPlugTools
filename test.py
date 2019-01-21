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
			'energy'   : '{"emeter":{"get_realtime":{}}}'
}

port = 9999
timeCmd    = commands["time"]
powerCmd   = commands["energy"]
turnOnCmd  = commands["on"]
turnOffCmd = commands["off"]

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
def turnOff(ip):
  print("turnOff(), ip = ", ip)

  turnOffResult = sendAndReceiveOnSocket(ip, port, turnOffCmd)
  decryptedTurnOffData = decrypt(turnOffResult[4:])
  
  turnOffRes = {'err_code' : int(findValueStr(decryptedTurnOffData, "err_code"))}
  
  print("TURN_OFF: E:{e:01d}"
      .format(e=turnOffRes["err_code"]))
  
  return turnOffRes

#python check_husqvarna.py -t 192.168.1.18 -c on
#('Sent:     ', '{"system":{"set_relay_state":{"state":1}}}')
#('Received: ', '{"system":{"set_relay_state":{"err_code":0}}}')
def turnOn(ip):
  print("turnOn(), ip = ", ip)

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
  
  
  print("TIME: {y:4d}-{m:02d}-{d:02d} {hr:02d}:{min:02d}:{sec:02d} E:{e:01d}"
      .format(y=dateTime["year"],
              m=dateTime["month"],
              d=dateTime["mday"],
              hr=dateTime["hour"],
              min=dateTime["min"],
              sec=dateTime["sec"],
              e=dateTime["err_code"]))
  
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
  
  print("POWER: I={i:5.5f} U={u:5.2f} P={p:5.5f} T={t:5.6f} E:{e:01d}"
        .format(i=power['current'],
                u=power['voltage'],
                p=power['power'],
                t=power['total'],
                e=power['err_code']))
  
  return power

# Parse commandline arguments
parser = argparse.ArgumentParser(description="TP-Link Wi-Fi Smart Plug Client v" + str(version))
parser.add_argument("-t", "--target", metavar="<hostname>", required=True, help="Target hostname or IP address", type=validHostname)

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-c", "--command", metavar="<command>", help="Preset command to send. Choices are: "+", ".join(commands), choices=commands)

group.add_argument("-j", "--json", metavar="<JSON string>", help="Full JSON string of command to send")

args = parser.parse_args()

# Set target IP, port and command to send
ip = args.target

# Turn OFF
turnOff  = turnOff(ip)
time.sleep(0.2)

# Turn ON
turnOn  = turnOn(ip)
time.sleep(0.2)

dateTime =getDateTime(ip)
power    =getPower(ip)

print("returned TURN_OFF: E:{e:01d}"
      .format(e=turnOff["err_code"]))

print("returned TURN_ON: E:{e:01d}"
      .format(e=turnOn["err_code"]))

print("returned TIME: {y:4d}-{m:02d}-{d:02d} {hr:02d}:{min:02d}:{sec:02d} E:{e:01d}"
      .format(y=dateTime["year"],
              m=dateTime["month"],
              d=dateTime["mday"],
              hr=dateTime["hour"],
              min=dateTime["min"],
              sec=dateTime["sec"],
              e=dateTime["err_code"]))

print("returned POWER: I={i:5.5f} U={u:5.2f} P={p:5.5f} E:{e:01d}"
      .format(i=power['current'],
              u=power['voltage'],
              p=power['power'],
              e=dateTime["err_code"]))
  
#print("{y:4d}-{m:02d}-{d:02d} {hr:02d}:{min:02d}:{sec:02d} {p:f}"
#      .format(y=date_year, m=date_month, d=date_mday,
#              hr=time_hour, min=time_min, sec=time_sec,
#              p=emeter_power))

