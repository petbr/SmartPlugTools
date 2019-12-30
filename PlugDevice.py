#!/usr/bin/env python2

import socket
import time
import enum
import argparse
import sys

from struct import pack

version = 0.2

# Predefined Smart Plug Commands
# For a full list of commands, consult tplink_commands.txt

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


####################################
class PlugDevice(object):
  
  # Class variables
  accessPort_C = 9999

  commands_C = {'info'     : '{"system":{"get_sysinfo":{}}}',
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

  port_C = 9999
  timeCmd_C    = commands_C["time"]
  powerCmd_C   = commands_C["energy"]
  turnOnCmd_C  = commands_C["on"]
  turnOffCmd_C = commands_C["off"]
  
  def __init__(self, name, hostName):
    self.name     = name
    self.hostName = hostName

# The opposite method of bytes.decode() is str.encode(),
# which returns a bytes representation of the Unicode string,
# encoded in the requested encoding.
  def sendAndReceiveOnSocket(self, ip, port, cmd):
    print("sendAndReceiveOnSocket")
    print("ip          =", ip)
    print("port        =", port)
    print("cmd         =", cmd)
    print("cmd(utf-8)  =", cmd.encode('utf-8'))
    
    try:
      # Connect socket
      sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock_tcp.connect((ip, port))
      bEncrCmd      = encrypt_str2b(cmd)
      print("sendAndReceiveOnSocket() SEND bEncrCmd               =", bEncrCmd)
      #bEncrCmd_encUtf8 = bEncrCmd.encode('utf-8')
#      bEncrCmd_encUtf8 = bEncrCmd
      sock_tcp.send( bEncrCmd )
      print("RECV")
      bytesData = sock_tcp.recv(2048)
      print("sendAndReceiveOnSocket RECV bytesData                =", bytesData)
#      strData = bytesData.decode('utf-8')
#      print("sendAndReceiveOnSocket RECV strData                  =", strData)

      #Close socket connection
      sock_tcp.close()

    except socket.error:
      quit("Cound not connect to host " + ip + ":" + str(port))

    return bytesData

  # python check_husqvarna.py -t 192.168.1.18 -c time
  # ('Sent:     ', '{"time":{"get_time":{}}}')
  # ('Received: ', '{"time":{"get_time":{"err_code":0,"year":2019,"month":1,"mday":21,"wday":1,"hour":19,"min":33,"sec":47}}}')
  def getDateTime(self):
      # print("getTime, ip = ", ip)

      timeData = self.sendAndReceiveOnSocket(self.hostName, self.port_C, self.timeCmd_C)
      decryptedTimeData = decrypt(timeData[4:])
      # print("decryptedTimeData = ", decryptedTimeData)

      dateTime = {'year': int(findValueStr(decryptedTimeData, "year")),
                  'month': int(findValueStr(decryptedTimeData, "month")),
                  'mday': int(findValueStr(decryptedTimeData, "mday")),
                  'hour': int(findValueStr(decryptedTimeData, "hour")),
                  'min': int(findValueStr(decryptedTimeData, "min")),
                  'sec': int(findValueStr(decryptedTimeData, "sec")),
                  'err_code': int(findValueStr(decryptedTimeData, "err_code"))}

      # print("TIME: {y:4d}-{m:02d}-{d:02d} {hr:02d}:{min:02d}:{sec:02d} E:{e:01d}"
      # .format(y=dateTime["year"],
      # m=dateTime["month"],
      # d=dateTime["mday"],
      # hr=dateTime["hour"],
      # min=dateTime["min"],
      # sec=dateTime["sec"],
      # e=dateTime["err_code"]))

      return dateTime

  #python check_husqvarna.py -t 192.168.1.18 -c energy
  #('Sent:     ', '{"emeter":{"get_realtime":{}}}')
  #('Received: ', '{"emeter":{"get_realtime":{"current":0.012866,"voltage":234.916847,"power":0.333881,"total":1.291000,"err_code":0}}}')

  #Ex. 1
  #getPower decryptedPowerData = {"emeter": {"get_realtime": {"current": 0.012711, "voltage": 237.028499, "power": 0, "total": 4.685000, "err_code": 0}}}

  #Ex. 2
  #getPower decryptedPowerData =  {"emeter":{"get_realtime":{"voltage_mv":233160,"current_ma":38,"power_mw":3739,"total_wh":1397,"err_code":0}}}
  def getPower(self):
    #print("getPower, ip = ", ip)

    print("getPower powerCmd_C = ", self.powerCmd_C)
    powerData = self.sendAndReceiveOnSocket(self.hostName, self.port_C, self.powerCmd_C)
    decryptedPowerData = decrypt(powerData[4:])
    print("getPower decryptedPowerData = ", decryptedPowerData)

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


##### class PlugDevice(object):

# Check if hostname is valid
def validHostname(hostname):
	try:
		socket.gethostbyname(hostname)
	except socket.error:
		parser.error("Invalid hostname.")
	return hostname

def dbgBytes(byteVal):
    i = 0
    for b in byteVal:
        print(i, " = ", chr(b), b)
        i = i + 1

# Encryption and Decryption of TP-Link Smart Home Protocol
# XOR Autokey Cipher with starting key = 171
def encrypt_str2b(strVal):
#  print("encrypt_str2b() str = ", strVal, "      len = ", len(strVal))
  key = 171
#  result = str(pack('>I', len(strVal)))
  result = len(strVal).to_bytes(4, byteorder='big')
#  print("encrypt_str2b() #1 result       = ", result)
#  print("encrypt_str2b() #1 type(result) = ", type(result))
  i = 0
  for c in strVal:
    a = key ^ ord(c)
#    print("a = ", a, "   c = ", c, "     i = ", i)
    key = a
    result += a.to_bytes(1, byteorder='big')
#    print("In loop result = ", result)
#    print("In loop size   = ", sys.getsizeof(result))
    i = i + 1

#  bResult = bytes(result, 'utf-8')

  return result

def decrypt(bytesData):
  
  #print("decrypt::string = ", string)
  key = 171
  result = ""

  i = 0
  for b in bytesData:
  #  print("decrypt b = ", b, "     bytesData = ", bytesData)
    a = key ^ b
  #  print("decrypt a = ", a, "   i = ", i)
    key = b
    result += chr(a)
  #  print("decrypt result = ", result)
    i = i + 1

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
  print(title)
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

  print("------------------------------------------")
  print("calcNewOffTime BW:{bw}, WT:{wt}, Wanted:{wa}".format(bw=sleepDurationBeforeWater,
                                                              wt=latestWaterTime,
                                                              wa=T_wantedPumpTime))
  print("ratio1 = {ra1}   ratio2 = {ra2}\n".format(ra1=ratio1, ra2=ratio2))
  print("=> new off time = {newOffT},".format(newOffT=t))
  print("------------------------------------------")
  
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
  T_pumpingAirBeforeTurnOff = 3
  T_reportAfterOffTime      = 2
  T_defaultMaxOffTime       = 120
  T_maxOffTime              = 10
  T_shortIdleTime           = 5
  T_lowResSleep             = 2
  T_mediumResSleep          = 1.0
  T_highResSleep            = 0.3

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

