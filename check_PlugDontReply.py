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
# python check_PlugDontReply.py -t 192.168.1.33 -c energy

import socket
import time
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
if args.command is None:
	cmd = args.json
else:
	cmd = commands[args.command]

def getSocket():
  socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  socket_tcp.settimeout(2)
  
  return socket_tcp

def connect(socket_tcp, ip, port):
  try:
    socket_tcp.connect((ip, port))
  except socket.error, msg:
    print "Couldnt connect with the socket-server: %s\n terminating program" % msg
    
  print "connect........BOTH!"
  

def tryCall():
  dataDecr = "Failing BAD...not yet understood"
  
  # Send command and receive reply
  try:
    sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_tcp.connect((ip, port))
    sock_tcp.send(encrypt(cmd))
    data = sock_tcp.recv(2048)
    sock_tcp.close()

    dataDecr = decrypt(data[4:])

    print ("Sent:     ", cmd)
    print ("Received: ", dataDecr)
    
  except socket.error:
    #quit("Cound not connect to host " + ip + ":" + str(port))
    print "Failing BAD in tryCall"

  return dataDecr

def tryCallSlim(socket_tcp):
  res = False;
  dataDecr = "Failing BAD...not yet understood"
  
  # Send command and receive reply
  try:
    socket_tcp.send(encrypt(cmd))
    data = socket_tcp.recv(2048)
    #socket_tcp.close()

    dataDecr = decrypt(data[4:])

    print ("Sent:     ", cmd)
    print ("Received: ", dataDecr)
    res = True
    
  except socket.error:
    #quit("Cound not connect to host " + ip + ":" + str(port))
    print "Failing BAD in tryCall"

  return (res,dataDecr)

print "Cmd:"
print cmd 

print "Socket bind"
socket_tcp = getSocket()

print "Connect"
connect(socket_tcp, ip, port)

print "Sleep\n"
time.sleep(5)
i = 1

print "TryCall ", i
i = i+1
res = False

while res == False:
  connect(socket_tcp, ip, port)
  (res,dataDecr) = tryCallSlim(socket_tcp)
  print "Res: ", res
  print "DataDecr: ", dataDecr, "\n"


print "Now I'm done!"

exit(1)

print "Sleep\n"
time.sleep(5)
print "TryCall ", i
i = i+1
data = tryCallSlim(socket_tcp)
print data, "\n"

print "Sleep\n"
time.sleep(5)
print "TryCall ", i
i = i+1
data = tryCallSlim(socket_tcp)
print data, "\n"

print "Sleep\n"
time.sleep(5)
print "TryCall ", i
i = i+1
data = tryCallSlim(socket_tcp)
print data, "\n"

print "Sleep\n"
time.sleep(5)
print "TryCall ", i
i = i+1
data = tryCallSlim(socket_tcp)
print data, "\n"

print "Sleep\n"
time.sleep(5)
print "TryCall ", i
i = i+1
data = tryCallSlim(socket_tcp)
print data, "\n"

print "Sleep\n"
time.sleep(5)
print "TryCall ", i
i = i+1
data = tryCallSlim(socket_tcp)
print data, "\n"

print "Sleep\n"
time.sleep(5)
print "TryCall ", i
i = i+1
data = tryCallSlim(socket_tcp)
print data, "\n"

print "Sleep\n"
time.sleep(5)
print "TryCall ", i
i = i+1
data = tryCallSlim(socket_tcp)
print data, "\n"

