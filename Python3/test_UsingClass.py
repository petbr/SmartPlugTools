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
plug1         = PlugDevice("Plug #1",         "192.168.1.31")
plug2         = PlugDevice("Plug #2",         "192.168.1.32")
plug3         = PlugDevice("Plug #3",         "192.168.1.33")

# Class variables
print("Access port_C:  {ap}"    .format(ap=PlugDevice.accessPort_C))
print("Commands_C:     {cmds}"  .format(cmds=PlugDevice.commands_C))
print("timeCmd_C:      {timeC}" .format(timeC=PlugDevice.timeCmd_C))
print("infoCmd_C:      {infoC}" .format(infoC=PlugDevice.infoCmd_C))
print("powerCmd_C:     {pwrC}"  .format(pwrC=PlugDevice.powerCmd_C))
print("turnOnCmd_C:    {tOnC}"  .format(tOnC=PlugDevice.turnOnCmd_C))
print("turnOffCmd_C:   {tOffC}" .format(tOffC=PlugDevice.turnOffCmd_C))


plug1Info = plug1.getInfo()["relay_state"]
print("plug1.getInfo = ", plug1Info)

# plug1.setPowerOff()
#plug1.setPowerOn(True)
#time.sleep(3.0)
#plug1.setPowerOff(True)

print("Petra was here!")
quit()

# Instance variables plug1
print("------------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------------")
print("Name     #1:            {name}"    .format(name     = plug1.name))
print("HostName #1:            {hostName}".format(hostName = plug1.hostName))
tMeasure = time.time()
print("tMeasure = {t}".format(t = tMeasure))
pPlug1 = plug1.getPower()
pPlug1['Time'] = tMeasure
print("Call Power Plug1:       {power}"   .format(power    = pPlug1))

# Instance variables plug2
print("------------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------------")
print("Name     #2:             {name}"    .format(name     = plug2.name))
print("HostName #2:             {hostName}".format(hostName = plug2.hostName))
tMeasure = time.time()
print("tMeasure = {t}".format(t = tMeasure))
pPlug2 = plug2.getPower()
pPlug2['Time'] = tMeasure
print("Call Power Plug1:        {power}"   .format(power     = pPlug2))

# Instance variables plug3
print("------------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------------")
print("Name     #3:             {name}"    .format(name     = plug3.name))
print("HostName #3:             {hostName}".format(hostName = plug3.hostName))
tMeasure = time.time()
print("tMeasure = {t}".format(t = tMeasure))
pPlug3 = plug3.getPower()
pPlug3['Time'] = tMeasure
print("Call Power Plug3:        {power}"   .format(power     = pPlug3))

# Instance variables Drainpump
print("------------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------------")
print("Name             DrainPump:  {name}"    .format(name     = plugDrainpump.name))
print("HostName         DrainPump:  {hostName}".format(hostName = plugDrainpump.hostName))
tMeasure = time.time()
print("tMeasure = {t}".format(t = tMeasure))
pPlugDp = plugDrainpump.getPower()
pPlugDp['Time'] = tMeasure
print("Call Power       DrainPump:  {power}"   .format(power    = pPlugDp))

print("tMeasure = ", tMeasure)

dtMeasure = datetime.fromtimestamp(tMeasure)

print("dtMeasure = ", dtMeasure)



t1 = time.time()
energy1       = {'Current': 0.028, 'Voltage': 234.962, 'Power': 1.965, 'Total': 10545, 'ErrCode': 0}
timeEnergy1   = {'Time': 1578508233.0543613, 'Energy' : energy1}

energy2       = {'Current': 0.028, 'Voltage': 234.962, 'Power': 1.965, 'Total': 10545, 'ErrCode': 0}
timeEnergy2   = {'Time': 1578508234.0543613, 'Energy' : energy2}

energy3       = {'Current': 0.028, 'Voltage': 234.962, 'Power': 1.965, 'Total': 10545, 'ErrCode': 0}
timeEnergy3   = {'Time': 1578508234.0543613, 'Energy' : energy3}

timeEnergy_arr = []
timeEnergy_arr.append(timeEnergy1)
timeEnergy_arr.append(timeEnergy2)
timeEnergy_arr.append(timeEnergy3)




energy1       = {'Current': 0.028, 'Voltage': 234.962, 'Power': 1.965, 'Total': 10545, 'ErrCode': 0}
timeEnergy1   = {'Time': 1578508233.0543613, 'Energy' : energy1}

energy2       = {'Current': 0.028, 'Voltage': 234.962, 'Power': 1.965, 'Total': 10545, 'ErrCode': 0}
timeEnergy2   = {'Time': 1578508234.0543613, 'Energy' : energy2}

energy3       = {'Current': 0.028, 'Voltage': 234.962, 'Power': 1.965, 'Total': 10545, 'ErrCode': 0}
timeEnergy3   = {'Time': 1578508234.0543613, 'Energy' : energy3}

timeEnergy_arr = []
timeEnergy_arr.append(timeEnergy1)
timeEnergy_arr.append(timeEnergy2)
timeEnergy_arr.append(timeEnergy3)



energy1       = {'Current': 0.028, 'Voltage': 234.962, 'Power': 1.965, 'Total': 10545, 'ErrCode': 0}
timeEnergy1   = {'Time': 1578508233.0543613, 'Energy' : energy1}

energy2       = {'Current': 0.028, 'Voltage': 234.962, 'Power': 1.965, 'Total': 10545, 'ErrCode': 0}
timeEnergy2   = {'Time': 1578508234.0543613, 'Energy' : energy2}

energy3       = {'Current': 0.028, 'Voltage': 234.962, 'Power': 1.965, 'Total': 10545, 'ErrCode': 0}
timeEnergy3   = {'Time': 1578508234.0543613, 'Energy' : energy3}

timeEnergy_arr = []
timeEnergy_arr.append(timeEnergy1)
timeEnergy_arr.append(timeEnergy2)
timeEnergy_arr.append(timeEnergy3)



energy1       = {'Current': 0.028, 'Voltage': 234.962, 'Power': 1.965, 'Total': 10545, 'ErrCode': 0}
timeEnergy1   = {'Time': 1578508233.0543613, 'Energy' : energy1}

energy2       = {'Current': 0.028, 'Voltage': 234.962, 'Power': 1.965, 'Total': 10545, 'ErrCode': 0}
timeEnergy2   = {'Time': 1578508234.0543613, 'Energy' : energy2}

energy3       = {'Current': 0.028, 'Voltage': 234.962, 'Power': 1.965, 'Total': 10545, 'ErrCode': 0}
timeEnergy3   = {'Time': 1578508234.0543613, 'Energy' : energy3}

timeEnergy_arr = []
timeEnergy_arr.append(timeEnergy1)
timeEnergy_arr.append(timeEnergy2)
timeEnergy_arr.append(timeEnergy3)





energy1       = {'Current': 0.028, 'Voltage': 234.962, 'Power': 1.965, 'Total': 10545, 'ErrCode': 0}
timeEnergy1   = {'Time': 1578508233.0543613, 'Energy' : energy1}

energy2       = {'Current': 0.028, 'Voltage': 234.962, 'Power': 1.965, 'Total': 10545, 'ErrCode': 0}
timeEnergy2   = {'Time': 1578508234.0543613, 'Energy' : energy2}

energy3       = {'Current': 0.028, 'Voltage': 234.962, 'Power': 1.965, 'Total': 10545, 'ErrCode': 0}
timeEnergy3   = {'Time': 1578508234.0543613, 'Energy' : energy3}

timeEnergy_arr = []
timeEnergy_arr.append(timeEnergy1)
timeEnergy_arr.append(timeEnergy2)
timeEnergy_arr.append(timeEnergy3)

t2 = time.time()

print("Time to create 5*timeEnergy_arr = ", t2-t1)

waitForZero = False
nrMeasurements = 0

filename = '/home/peter/repo/SmartPlugTools/te_arr_json2'

te_arr = []
te_arr = loadData(filename)

# Retrieve the previous measurement
tMeasurePrev = te_arr[-1]['Time']
print('----------------------------')
print('----------------------------')
print('----------------------------')
print('Most recent measure = ', te_arr[-1])
print('----------------------------')
print('----------------------------')
print('----------------------------')

# 0
# m1      Previous   #1
# m2
# 0       Report
# 0
# m1      Previous   #2
# m2
# m3
# m4
# 0       Report
# 0

def convertFile(filename, arr):
  print("Convert ", filename)

  tMeasureFirst = arr[0]['Time']
  tMeasurePrev = tMeasureFirst - 200
  dtFirst = datetime.fromtimestamp(tMeasureFirst)
  convArr = []
  for e in arr:
    tMeasure = e['Time']
    dt = datetime.fromtimestamp(tMeasure)
    print("item = ", e, "tMeasure = ", tMeasure,  "   dt =  ", dt)
    eToAdd = e
    if e['Energy']['Power'] == 0:
      tSleep = tMeasure - tMeasurePrev
      tMeasurePrev = tMeasure
      if e.get('TimeSleep') == None:
        print("TimeSleep is missing, ADD IT")
        eToAdd['TimeSleep'] = tSleep
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

    print("eToAdd  = ", eToAdd)

    convArr.append(eToAdd)

  saveData(filename, convArr)


#convertFile(filename, te_arr)

#exit(0)

def invertPlug1():
  plug1Info_Relay_state = plug1.getInfo()["relay_state"]
  if plug1Info_Relay_state == 0:
    plug1.setPowerOn()
  else:
    plug1.setPowerOff()

invertPlug1()
time.sleep(0.05)
invertPlug1()

sleepTime = 2
while True:
  tMeasure    = time.time()
  ePlugDp = plugDrainpump.getPower()
  nrMeasurements = nrMeasurements + 1

  # Report non zero power or if zero hasn't been observed since before
  if (ePlugDp['Power'] > 0) or (waitForZero == True):
    sleepTime = 0.5
    if (ePlugDp['Power'] == 0):
#      if waitForZero == True:
#        invertPlug1()

      waitForZero = False

      tSleep = tMeasure - tMeasurePrev
      te = {'Time': tMeasure, 'TimeSleep': tSleep, 'Energy': ePlugDp}
      te_arr.append(te)
      saveData(filename, te_arr)

      tMeasurePrev = tMeasure

    else:
      if waitForZero == False:
        invertPlug1()
        time.sleep(0.05)
        invertPlug1()


      te = {'Time': tMeasure, 'Energy': ePlugDp}
      te_arr.append(te)
      waitForZero = True
      sleepTime = 5

    dt = datetime.fromtimestamp(tMeasure)
    print("--------------------", nrMeasurements, "-----------------------")
    print("--------------------", nrMeasurements, "-----------------------")
    print("--------------------", nrMeasurements, "-----------------------")
    print("--------------------", nrMeasurements, "-----------------------")
    print("--------------------", nrMeasurements, "-----------------------")
    print("tMeasure         = ", tMeasure, "      ", dt)
    print("ePlugDp          = ", ePlugDp)
    print("te               = ", te)
    print("Length of te_arr = ", len(te_arr))
    print("Size of te_arr   = ", sys.getsizeof(te_arr))

  time.sleep(sleepTime)
    
