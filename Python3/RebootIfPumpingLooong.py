#!/usr/bin/env python2
#
# Wanted features
# *
#
import time
import sys
import json
from datetime import datetime
from PlugDevice import PlugDevice

def printArr(arr):
  for e in arr:
    t = e['Time']
    dt = datetime.fromtimestamp(t)
    p  = e['Energy']['Power']
    tot = e['Energy']['Total']
    print('T=', t, '(', dt, ')', 'P=', p, 'Total=', tot)

def printArrPower(arr):
  for e in arr:
    t = e['Time']
    dt = datetime.fromtimestamp(t)
    p  = e['Energy']['Power']
    print('T=', t, '(', dt, ')', 'P=', p)

def printArrTotal(arr):
  for e in arr:
    t = e['Time']
    dt  = datetime.fromtimestamp(t)
    tot = e['Energy']['Total']
    print('T=', t, '(', dt, ')', 'Total=', tot)

def saveData(filename, data):
  with open(filename, 'w') as outfile:
    data_json = json.dumps(data)
    json.dump(data_json, outfile)

def loadData(filename):
  with open(filename) as json_file:
    data_json = json.load(json_file)
    data = json.loads(data_json)
    return data

print("Starting tester!")

plugDrainpump = PlugDevice("Plug #Drainpump", "192.168.1.18")

# Class variables
print("Access port_C:  {ap}"      .format(ap      = PlugDevice.accessPort_C))
print("Commands_C:     {cmds}"    .format(cmds    = PlugDevice.commands_C))
print("timeCmd_C:      {timeC}"   .format(timeC   = PlugDevice.timeCmd_C))
print("infoCmd_C:      {infoC}"   .format(infoC   = PlugDevice.infoCmd_C))
print("powerCmd_C:     {pwrC}"    .format(pwrC    = PlugDevice.powerCmd_C))
print("turnOnCmd_C:    {tOnC}"    .format(tOnC    = PlugDevice.turnOnCmd_C))
print("turnOffCmd_C:   {tOffC}"   .format(tOffC   = PlugDevice.turnOffCmd_C))
print("rebootCmd_C:    {rebootC}" .format(rebootC = PlugDevice.rebootCmd_C))
print("rebootCmd_C:    {rebootC}" .format(rebootC = PlugDevice.rebootCmd_C))


print("plugDrainpump.getInfo = ", plugDrainpump.getInfo())
print("\n\n")
#print("plug1.getInfo() = ", plug1.getInfo())
#print("plug2.getInfo() = ", plug2.getInfo())
#print("plug3.getInfo() = ", plug3.getInfo())

# plug1.setPowerOff()
#plug1.setPowerOn(True)
#time.sleep(3.0)
#plug1.setPowerOff(True)

print("Petra was here!!!!!!!!!!!             !!!!!!!!!!")

powerData = plugDrainpump.getPower()
justPower = powerData['Power']

info = plugDrainpump.getInfo()

print("Info drainpump: ", info)
print("PowerData:      ", powerData)
print("Power:          ", justPower)

lowAirpumpTreshold  = 10
highAirpumpTreshold = 250
contRunning = True
while contRunning:
  dateTime =  plugDrainpump.getDateTime()
  powerData = plugDrainpump.getPower()
  justPower = powerData['Power']

  print("DateTime:       ", dateTime)
  print("PowerData:      ", powerData)
  print("Power:          ", justPower)
  print("")

  if justPower>highAirpumpTreshold:
    print("Working high")
    print("Working high")
    print("Working high")
    print("Working high")
    print("Working high")
    print("Working high")
    print("Working high")

  if (justPower>lowAirpumpTreshold) and (justPower<highAirpumpTreshold):
    print("Pumping AIR!!!!!!!!!!!!!!")
    print("Pumping AIR!!!!!!!!!!!!!!")
    print("Pumping AIR!!!!!!!!!!!!!!")
    print("Pumping AIR!!!!!!!!!!!!!!")
    print("Pumping AIR!!!!!!!!!!!!!!")
    print("Pumping AIR!!!!!!!!!!!!!!")
    print("Pumping AIR!!!!!!!!!!!!!!")

  if (justPower<lowAirpumpTreshold):
    print("Idle")


  time.sleep(1)
	
quit()






