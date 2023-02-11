#!/usr/bin/env python2
#
# Wanted features
# *
#
import os
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

pumpAirTimer = False
pumpAirStart = -1


def TurnOffAirTimer():
  global pumpAirTimer
  global pumpAirStart

  pumpAirTimer = False
  pumpAirStart = -1
  cmd = "touch /var/log/DranpumpData/REBOOT_TurnOffAirTimer"
  returned_value = os.system(cmd)  # returns the exit code in unix

def StartAirTimer():
  global pumpAirTimer
  global pumpAirStart

  print("StartAirTimer()")
  if pumpAirTimer == False:
    pumpAirTimer = time.time()
 
  pumpAirTimer = True
  timeInAir = time.time() - pumpAirTimer
  
  cmd = "touch /var/log/DranpumpData/REBOOT_StartAirTimer"
  returned_value = os.system(cmd)  # returns the exit code in unix
  print('StartAirTimer, returned value:', returned_value)
  print('StartAirTimer, timeInAir:', timeInAir)
  
  if timeInAir > 10:
    cmd = "touch /var/log/DranpumpData/REBOOT"
    returned_value = os.system(cmd)  # returns the exit code in unix
    print('StartAirTimer(), returned value:', returned_value)
    print("I am in AIR tooo long!")



lowAirpumpTreshold  = 10
highAirpumpTreshold = 250
contRunning = True
while contRunning:
  dateTime =  plugDrainpump.getDateTime()
  powerData = plugDrainpump.getPower()
  justPower = powerData['Power']

  if justPower>highAirpumpTreshold:
    print("DateTime:       ", dateTime)
    print("PowerData:      ", powerData)
    print("Power:          ", justPower)
    print("")
    print("Working high")
    TurnOffAirTimer()
    cmd = "touch /var/log/DranpumpData/REBOOT_PUMPING"
    returned_value = os.system(cmd)  # returns the exit code in unix
    print('PUMPING, returned value:', returned_value)

  if (justPower>lowAirpumpTreshold) and (justPower<highAirpumpTreshold):
    print("DateTime:       ", dateTime)
    print("PowerData:      ", powerData)
    print("Power:          ", justPower)
    print("")
    print("Pumping AIR!!!!!!!!!!!!!!")
    StartAirTimer()

  if (justPower<lowAirpumpTreshold):
    TurnOffAirTimer()
    cmd = "touch /var/log/DranpumpData/REBOOT_Idle"
    returned_value = os.system(cmd)  # returns the exit code in unix

  time.sleep(1)
	
quit()






