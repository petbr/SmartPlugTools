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
# python tplink_smartplug.py -t 192.168.1.75 -c energy

import socket
import argparse
from struct import pack

version = 0.2

# Check if hostname is valid
def validHostname(hostname):
	try:
		socket.gethostbyname(hostname)
	except socket.error:
		parser.error("Invalid hostname.")
	return hostname

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


# Parse commandline arguments
parser = argparse.ArgumentParser(description="TP-Link Wi-Fi Smart Plug Client v" + str(version))
parser.add_argument("-t", "--target", metavar="<hostname>", required=True, help="Target hostname or IP address", type=validHostname)

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-c", "--command", metavar="<command>", help="Preset command to send. Choices are: "+", ".join(commands), choices=commands)

group.add_argument("-j", "--json", metavar="<JSON string>", help="Full JSON string of command to send")

args = parser.parse_args()

# Set target IP, port and command to send
ip = args.target
port = 9999
timeCommand   = "time"
energyCommand = "energy"

timeCmd   = commands[timeCommand]
energyCmd = commands[energyCommand]

timeData   = sendAndReceiveOnSocket(ip, port, timeCmd)
decryptedTimeData = decrypt(timeData[4:])
# print("decryptedTimeData = ", decryptedTimeData)

energyData = sendAndReceiveOnSocket(ip, port, energyCmd)
decryptedEnergyData = decrypt(energyData[4:])
# print("decryptedEnergyData = ", decryptedEnergyData)

# print("findTime   = ", findValueStr(decryptedTimeData,   "sec"))
# print("findEnergy = ", findValueStr(decryptedEnergyData, "power"))

date_year  = int(findValueStr(decryptedTimeData,   "year"))
date_month = int(findValueStr(decryptedTimeData,   "month"))
date_mday  = int(findValueStr(decryptedTimeData,   "mday"))
#print("year: ", date_year, "   month: ", date_month, "   mday: ", date_mday)

time_hour = int(findValueStr(decryptedTimeData, "hour"))
time_min  = int(findValueStr(decryptedTimeData, "min"))
time_sec  = int(findValueStr(decryptedTimeData, "sec"))
#print("hour: ", time_hour, "   min: ", time_min, "   sec: ", time_sec)

emeter_current = float(findValueStr(decryptedEnergyData, "current"))
emeter_voltage = float(findValueStr(decryptedEnergyData, "voltage"))
emeter_power   = float(findValueStr(decryptedEnergyData, "power"))
#print("current: ", emeter_current, "   voltage: ", emeter_voltage, "   power: ", emeter_power)

print("{y:4d}-{m:02d}-{d:02d} {hr:02d}:{min:02d}:{sec:02d} {p:f}"
      .format(y=date_year, m=date_month, d=date_mday,
              hr=time_hour, min=time_min, sec=time_sec,
              p=emeter_power))

