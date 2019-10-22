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
# python test.py -t 192.168.1.18 -c energy | tee ful_log.txt
#
# ~/repo/SmartPlugTools
#
# Start web server
# *1* python -m SimpleHTTPServer 8000
# *2* webfsd -F -p 5000
#
# Start VNC viewer
# ~/Downloads/VNC-Viewer-6.19.107-Linux-x64
# 
# Raspberry web server
# /etc/lighttpd/lighttpd.conf
#
# Lighttpd config file
# /etc/lighttpd/lighttpd.conf
# Restart web server
# /etc/init.d/lighttpd restart
# Use /tmp/DranpumpData as data storage place
#
# redis-server
# /etc/init.d/redis-server restart
# /etc/init.d/redis-server stop
# /etc/init.d/redis-server start

import socket
import time
import datetime
import enum
import argparse
import sys

from struct import pack

version = 0.9

sendAndReceiveErrorsCounter = 0

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
  
  #print("decrypt::string = ", string)
  key = 171
  result = ""
  
  for i in string:
    a = key ^ ord(i)
    key = ord(i)
    result += chr(a)

  #print("decrypt::result = ", result)
  
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
  global sendAndReceiveErrorsCounter

  faultyTimes = 0
  successfulSend = False
  data = "Didn't work out, will be set later"
  
  while successfulSend == False:
    try:
      # Connect socket

      sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock_tcp.connect((ip, port))
      sock_tcp.send(encrypt(cmd))
      data = sock_tcp.recv(2048)
      
      #Close socket connection
      sock_tcp.close()
      successfulSend = True
      
#    except socket.error:
    except:
      faultyTimes = faultyTimes + 1
      print(datetime.datetime.now())
      print("sendAndReceiveOnSocket::  time = " + str(time.time()))
      sys.stdout.flush()
      
      print("Coulllllllllllld not connect to host " + ip + ":" + str(port))
      sys.stdout.flush()
      print("except Try #", str(faultyTimes))
      sys.stdout.flush()
      successfulSend = False
    
  if faultyTimes > sendAndReceiveErrorsCounter:
    sendAndReceiveErrorsCounter = faultyTimes
    print("sendAndReceiveOnSocket:: Tried too much current max #", str(sendAndReceiveErrorsCounter))
    
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
  #print("getDateTime::timeData = ", timeData)
  decryptedTimeData = decrypt(timeData[4:])
  #print("decryptedTimeData = ", decryptedTimeData)
  
  dateTime = {'year'     : int(findValueStr(decryptedTimeData,  "year")),
              'month'    : int(findValueStr(decryptedTimeData,  "month")),
              'mday'     : int(findValueStr(decryptedTimeData,  "mday")),
              'hour'     : int(findValueStr(decryptedTimeData,  "hour")),
              'min'      : int(findValueStr(decryptedTimeData,  "min")),
              'sec'      : int(findValueStr(decryptedTimeData,  "sec")),
              'err_code' : int(findValueStr(decryptedTimeData, "err_code"))}
  
#Traceback (most recent call last):
#  File "test.py", line 617, in <module>
#    dateTime = getDateTime(ip)
#  File "test.py", line 192, in getDateTime
#    dateTime = {'year'     : int(findValueStr(decryptedTimeData,  "year")),
#ValueError: invalid literal for int() with base 10: ''

  
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

def getGraphListFileName(dateTime,
                         tPumpAirBeforeTurnOff,
                         tMaxOffTime,
                         tShortIdleTime,
                         waterTime, sleepDurationBeforeWater, isOffByItself):
  
  filename = "/tmp/DranpumpData/{y:04d}-{m:02d}-{d:02d}_{hr:02d}m{min:02d}_AirBOff:{t1:02d}_tMaxOff:{t2:03d}_tShortIdle:{t3:02d}_BW:{bw:4.2f}_WT:{wt:2.2f}".format(y=dateTime["year"],
              m=dateTime["month"],
              d=dateTime["mday"],
              hr=dateTime["hour"],
              min=dateTime["min"],
              t1=tPumpAirBeforeTurnOff, t2=tMaxOffTime, t3=tShortIdleTime,
              bw=sleepDurationBeforeWater,
              wt=waterTime)
  
  if isOffByItself:
    filename = filename + "__Good.html"
  else:
    filename = filename + ".html"
    
  return filename
  

def getGraphItem(dateTime, power):
  s = "['{hr:02d}:{min:02d}:{sec:02d}', {p}],".format(hr=dateTime['hour'],
                                                   min=dateTime['min'],
                                                   sec=dateTime['sec'],
                                                   p=power['power'])
  return s

def createHtmlContents(listOfGraphItems, title):
  print title
  #title = "title: 'Dranpump (W)'"
  cnts =        "<html>\n"
  cnts = cnts + "  <head>\n"
  cnts = cnts + "      <script type=\"text/javascript\" src=\"https://www.gstatic.com/charts/loader.js\"></script>\n"
  cnts = cnts + "      <script type=\"text/javascript\">\n"
  cnts = cnts + "      google.charts.load('current', {'packages':['corechart']});\n"
  cnts = cnts + "      google.charts.setOnLoadCallback(drawChart);\n"
  cnts = cnts + "\n"
  cnts = cnts + "      function drawChart() {\n"
  cnts = cnts + "        var data = google.visualization.arrayToDataTable([\n"
  cnts = cnts + "                    ['Tid',  'Effekt'],\n"
  cnts = cnts + listOfGraphItems + "\n"
  cnts = cnts + "        ]);\n"
  cnts = cnts + "\n"
  cnts = cnts + "        var options = {\n"
  cnts = cnts + title + ",\n"   
  cnts = cnts + "          curveType: 'function',\n"
  cnts = cnts + "          lineWidth: 5,\n"
  cnts = cnts + "          legend: { position: 'bottom' }\n"
  cnts = cnts + "        };\n"
  cnts = cnts + "\n"
#  cnts = cnts + "        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));\n"
  cnts = cnts + "        var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));\n"
  cnts = cnts + "\n"
  cnts = cnts + "        chart.draw(data, options);\n"
  cnts = cnts + "      }\n"
  cnts = cnts + "    </script>\n"
  cnts = cnts + "  </head>\n"
  cnts = cnts + "  <body>\n"
#  cnts = cnts + "    <div id=\"curve_chart\" style=\"width: 1800px; height: 800px\"></div>\n"
  cnts = cnts + "    <div id=\"chart_div\" style=\"width: 100%; height: 100%\"></div>\n"
  cnts = cnts + "  </body>\n"
  cnts = cnts + "</html>\n"
  return cnts

def createFile(filename, contents):
  global sendAndReceiveErrorsCounter
  print("sendAndReceiveOnSocket:: Tried too much current max #", str(sendAndReceiveErrorsCounter))
  
  f = open(filename, "w+")
  f.write(contents)
  f.close()
  
  print("File: " + filename + " created!")
  t = time.time()
  
  ###############
  #est_WakeupTime = t + datetime.timedelta(0,T_maxOffTime)
  #print("Estimated wake up time: " + est_WakeupTime)
  
  sys.stdout.flush()
  
  return

def calcNewOffTime(sleepDurationBeforeWater, latestWaterTime):
  return T_defaultMaxOffTime

  # Typical at start the values == 0...then use default
  if (sleepDurationBeforeWater == 0) or (latestWaterTime == 0):
    t = T_defaultMaxOffTime
  else:
    # Ex wanted = 8, latest = 4     => ration = 2
    # Ex wanted = 8, latest = 16    => ration = 0.5
    ratio1 = T_wantedPumpTime / latestWaterTime
    
    # If ration < 1 use ratio = ration^2
    # ratio #1 = 2   => ration #2 = 2          Don't change
    # ratio #1 = 0.5 => ration #2 = 0.25       Change with ^2
    if ratio1 < 1.0:
      ratio2 = ratio1 * ratio1
    else:
      ratio2 = ratio1
      
    t = int(sleepDurationBeforeWater * ratio2)
    if t < T_defaultMaxOffTime :
      t = T_defaultMaxOffTime

  ##########################
  # NO! Always use default!
  ##########################
  #t = T_defaultMaxOffTime

  print "------------------------------------------"
  print "calcNewOffTime BW:{bw}, WT:{wt}, Wanted:{wa}".format(bw=sleepDurationBeforeWater,
                                                              wt=latestWaterTime,
                                                              wa=T_wantedPumpTime)
  print "ratio1 = {ra1}   ratio2 = {ra2}\n".format(ra1=ratio1, ra2=ratio2)
  print "=> new off time = {newOffT},".format(newOffT=t)
  print "------------------------------------------"
  
  return t


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
  print("returned POWER @ On: I={i:5.5f} U={u:5.2f} P={p:5.5f}  Tot={tot:5.5f} E:{e:01d}"
        .format(i=powerAtOn['current'],
                u=powerAtOn['voltage'],
                p=powerAtOn['power'],
                tot=powerAtOn['total'],
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
  print("POWER I={i:5.5f} U={u:5.2f} P={p:5.5f} Tot={tot:5.5f} E:{e:01d}"
        .format(i=pwr['current'],
                u=pwr['voltage'],
                p=pwr['power'],
                tot=pwr['total'],
                e=pwr["err_code"]))
  return

def printPumpMode(pumpMode):
  print ("Pump mode = {pm:s}"
         .format(pm=pumpMode.name))
  return

def printStatus(directive, duration,
                dateTime, pwr, mode, tMaxOffTime):

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
  print ("Shortest time pumping water      = {t}"
         .format(t=shortestPumpWaterDuration))
  print ("Longest time pumping water       = {t}"
         .format(t=longestPumpWaterDuration))
  print ("Shortest time pumping air        = {t}"
         .format(t=shortestPumpAirDuration))
  print ("Longest time pumping air         = {t}"
         .format(t=longestPumpAirDuration))
  print ("Counter short to pump            = {c}"
         .format(c=C_shortIdleToPump))
  print ("Counter long to pump             = {c}"
         .format(c=C_longIdleToPump))
  print ("Times: T_pumpingAirBeforeTurnOff = {t}"
         .format(t=T_pumpingAirBeforeTurnOff))
  print ("Times: T_maxOffTime              = {t}"
         .format(t=T_maxOffTime))
  print ("Times: T_shortIdleTime           = {t}"
         .format(t=T_shortIdleTime))
  print ("Sleep time prospect              = {t}"
         .format(t=sleepTimeProspect))
  print ("Sleep duration before water      = {t}"
         .format(t=sleepDurationBeforeWater))
  print ("T_wantedPumpTime                 = {t}"
         .format(t=T_wantedPumpTime))
  print ("tMaxOffTime                      = {t}"
         .format(t=tMaxOffTime))
  
  printPower(pwr)
  printPumpMode(mode)
  print(directive)

  sys.stdout.flush()
 
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



# idle -> pumpingWater -> pumpingAir/idle -> idle

def switchMode(pm, dt, pow):
  global pumpMode

  pumpMode = pm
  powVal = pow['power']

def startup():
  # Power tresholds
  global P_idleTreshold
  global P_airPumpingTreshold
  global P_waterPumpingTreshold

  # Time tresholds.
  global T_wantedPumpTime
  global T_minPumpingWater
  global T_pumpingAirBeforeTurnOff
  global T_reportAfterOffTime
  global T_defaultMaxOffTime
  global T_maxOffTime
  global T_shortIdleTime
  global T_lowResSleep
  global T_mediumResSleep
  global T_highResSleep

  # Counter
  global C_shortIdleToPump
  global C_longIdleToPump

  global powerState
  global pumpMode
  global contRunning
  global prevPower
  global shortestIdleShortDuration
  global longestIdleShortDuration
  global shortestIdleLongDuration
  global longestIdleLongDuration
  global shortestPumpWaterDuration
  global longestPumpWaterDuration
  global shortestPumpAirDuration
  global longestPumpAirDuration
  global switchTime
  global dateTime
  global power
  global isVirginList
  global listOfGraphItems
  global latestWaterTime
  global sleepTimeProspect
  global sleepDurationBeforeWater

  # Power tresholds
  P_idleTreshold = 20
  P_airPumpingTreshold = 320
  P_waterPumpingTreshold = 350

  # Time tresholds.
  T_wantedPumpTime          = 7.0
  T_minPumpingWater         = 2
  T_pumpingAirBeforeTurnOff = 10
  T_reportAfterOffTime      = 2
  T_defaultMaxOffTime       = 120
  T_maxOffTime              = 10
  T_shortIdleTime           = 5
#  T_lowResSleep             = 2
#  T_mediumResSleep          = 1.0
#  T_highResSleep            = 0.3
  T_lowResSleep             = 4
  T_mediumResSleep          = 2.0
  T_highResSleep            = 1.0

  # Counter
  C_shortIdleToPump = 0
  C_longIdleToPump  = 0
  #class PumpMode(enum.Enum): 
  #idle          = 1
  #pumpingAir    = 2
  #pumpTurnedOff = 3
  #pumpingWater  = 4

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
  dateTime = getDateTime(ip)
  power    = getPower(ip)
  isVirginList = True
  listOfGraphItems = ""
  latestWaterTime = 0
  sleepTimeProspect = time.time()
  sleepDurationBeforeWater = 0

  setTurnOn(ip)
  printStatus("Just started ====> Turn ON and Idle short!\n", 0,
              dateTime, power, pumpMode, T_maxOffTime)


print "*********************************************"
print "*********************************************"
print "!!!!!!!!!!!!!!!!!!!STARTING!!!!!!!!!!!!!!!!!!"
print "*********************************************"
print "*********************************************"

startup()
while contRunning:
  dateTime = getDateTime(ip)
  power    = getPower(ip)
  powerValue = power['power']

#  print "{hr:2d}:{m:2d}.{s:2d}   Pump mode = {pm:10s}   P={p:5.5f}".format(hr=dateTime["hour"],
#                                                                           m=dateTime["min"],
#                                                                           s=dateTime["sec"],
#                                                                           pm=pumpMode.name,
#                                                                           p=powerValue)
  sys.stdout.flush()

  if (pumpMode is PumpMode.idle_short):
    changeTime = time.time()
    duration = changeTime-switchTime
    if powerValue > P_idleTreshold:
      shortestIdleShortDuration = min(duration, shortestIdleShortDuration)
      longestIdleShortDuration  = max(duration, longestIdleShortDuration)
      switchTime = changeTime
      C_shortIdleToPump = C_shortIdleToPump + 1
      sleepDurationBeforeWater = changeTime - sleepTimeProspect
      printStatus("Idle short ===> Pumping water\n", duration,
                  dateTime, power, pumpMode, T_maxOffTime)

      switchMode(PumpMode.pumpingWater, dateTime, power)
      
    elif duration > T_shortIdleTime:
      printStatus("Short idle ===> Idle long\n", duration,
                  dateTime, power, pumpMode, T_maxOffTime)
      switchMode(PumpMode.idle_long, dateTime, power)
      
  elif pumpMode is PumpMode.idle_long:

    changeTime = time.time()
    if isVirginList:
      # Report the current list of graph items and start a new one     
      title  = "          title: 'Dranpump (W) tOffTime={t_off:03d}  "
      title += "waterTime={waterTime:2.2f}'"
      title = title.format(t_off=T_maxOffTime, waterTime=latestWaterTime)
      print title
      contents = createHtmlContents(listOfGraphItems, title)
      filename = getGraphListFileName(dateTime,
                                      T_pumpingAirBeforeTurnOff,
                                      T_maxOffTime,
                                      T_shortIdleTime,
                                      latestWaterTime,
                                      sleepDurationBeforeWater,
                                      True)
      print "Filename: " + filename + "\n"
      print "Contents: " + contents + "\n"
      createFile(filename, contents)
      listOfGraphItems = ""
      sys.stdout.flush()
    
      # A new one must be started
      isVirginList = False
      listOfGraphItems = ""

#
    duration = changeTime-switchTime
    if powerValue > P_idleTreshold:
      shortestIdleLongDuration = min(duration, shortestIdleLongDuration)
      longestIdleLongDuration  = max(duration, longestIdleLongDuration)
      switchTime = changeTime
      C_longIdleToPump = C_longIdleToPump + 1
      sleepDurationBeforeWater = changeTime - sleepTimeProspect      
      printStatus("Idle Long ===> Pumping water\n", duration,
                  dateTime, power, pumpMode, T_maxOffTime)
      switchMode(PumpMode.pumpingWater, dateTime, power)

      
  elif pumpMode is PumpMode.pumpingWater:
    isVirginList = True
    
    #print ("Pumping water, P={p:5.5f}"
    #       .format(p=powerValue))
    changeTime = time.time()      
    duration = changeTime-switchTime
    if (powerValue < P_airPumpingTreshold) and (duration >= T_minPumpingWater):
      shortestPumpWaterDuration = min(duration, shortestPumpWaterDuration)
      longestPumpWaterDuration = max(duration, longestPumpWaterDuration)
      switchTime = changeTime
      latestWaterTime = duration
      printStatus("Pumping water ===> Pumping air\n", duration,
                  dateTime, power, pumpMode, T_maxOffTime)

      switchMode(PumpMode.pumpingAir, dateTime, power)
    
  elif pumpMode is PumpMode.pumpingAir:
    #print ("Pumping air, P={p:5.5f}"
    #       .format(p=powerValue))
    timePumpingAir = time.time()-switchTime
    if powerValue < P_idleTreshold:
      sleepTimeProspect = time.time()
      duration = sleepTimeProspect-switchTime
      shortestPumpAirDuration = min(duration, shortestPumpAirDuration)
      longestPumpAirDuration  = max(duration, longestPumpAirDuration)
      switchTime = sleepTimeProspect
      printStatus("Pumping Air short time ===> Idle short\n", duration,
                  dateTime, power, pumpMode, T_maxOffTime)

      switchMode(PumpMode.idle_short, dateTime, power)

    elif timePumpingAir > T_pumpingAirBeforeTurnOff:
      sleepTimeProspect = time.time()      
      duration = sleepTimeProspect-switchTime
      shortestPumpAirDuration = min(duration, shortestPumpAirDuration)
      longestPumpAirDuration  = max(duration, longestPumpAirDuration)
      
      T_maxOffTime = calcNewOffTime(sleepDurationBeforeWater,
                                    latestWaterTime)
      setTurnOff(ip)    
      switchTime = sleepTimeProspect      
      printStatus("Pumping Air too long time ===> Turn OFF!!!!\n", duration,
                  dateTime, power, pumpMode, T_maxOffTime)

      switchMode(PumpMode.pumpTurnedOff, dateTime, power)
    
  elif pumpMode is PumpMode.pumpTurnedOff:
    #print ("Pump turned off, P={p:5.5f}"
    #       .format(p=powerValue))
    offDuration = time.time() - switchTime      

    if (offDuration > T_reportAfterOffTime):

      # Maybe user remotely did start the pump....
      if powerValue > P_idleTreshold:
        startup()

      if isVirginList:
        # Report the current list of graph items and start a new one
        title  = "          title: 'Dranpump (W) tOffTime={t_Off:4d}"
        title += "  waterTime={wt:4.2f}'"
        title = title.format(t_Off=T_maxOffTime, wt=latestWaterTime)
        print title
        contents = createHtmlContents(listOfGraphItems, title)
        
        
        filename = getGraphListFileName(dateTime,
                                        T_pumpingAirBeforeTurnOff,
                                        T_maxOffTime,
                                        T_shortIdleTime,
                                        latestWaterTime,
                                        sleepDurationBeforeWater,
                                        False)
        print "Filename: " + filename + "\n"
        print "Contents: " + contents + "\n"
        createFile(filename, contents)
        listOfGraphItems = ""
        sys.stdout.flush()
      
        # A new one must be started
        isVirginList = False
        listOfGraphItems = ""

    if offDuration > T_maxOffTime:
      changeTime = time.time()      
      print ("Duration = {t:5.2f}"
              .format(t=offDuration))
      setTurnOn(ip)
      switchTime = changeTime
      printStatus("OFF max time reached ===> Turn ON + Idle short!!!!\n", offDuration,
                  dateTime, power, pumpMode, T_maxOffTime)
      switchMode(PumpMode.idle_short, dateTime, power)
    
  else:
    print ("Pump mode = UNKNOWN, go to Idle")
    changeTime = time.time()
    duration = changeTime-switchTime
    switchTime = changeTime
    setTurnOn(ip)
    printStatus("OFF max time reached ===> Turn ON + Idle!!!!\n", duration,
                dateTime, power, pumpMode, T_maxOffTime)
    switchMode(PumpMode.idle_short, dateTime, power)
      
  # Echo mode when turned OFF....but when not getting close to end time.
  offDuration = time.time() - switchTime      
  # Have medium resolution when idle_long
  if pumpMode == PumpMode.idle_long:
    time.sleep(T_mediumResSleep)
  elif pumpMode == PumpMode.pumpTurnedOff:
    # When turned off and start to get close end time....have high resolution
    if (offDuration+5) > T_maxOffTime:
      print "Getting close...  ", (T_maxOffTime-offDuration)
      time.sleep(T_highResSleep)
    else:
      time.sleep(T_lowResSleep)
  else:
    if isVirginList:
      gItem = getGraphItem(dateTime, power)
      listOfGraphItems = listOfGraphItems + "\n" + gItem
      #sys.stdout.flush()
    time.sleep(T_highResSleep)

  prevPower = powerValue

#print("{y:4d}-{m:02d}-{d:02d} {hr:02d}:{min:02d}:{sec:02d} {p:f}"
#      .format(y=date_year, m=date_month, d=date_mday,
#              hr=time_hour, min=time_min, sec=time_sec,
#              p=emeter_power))

