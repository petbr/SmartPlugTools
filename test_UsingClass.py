#!/usr/bin/env python2
#
import time
import sys
import json
from datetime import datetime
from PlugDevice import PlugDevice


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
print("powerCmd_C:     {pwrC}"  .format(pwrC=PlugDevice.powerCmd_C))
print("turnOnCmd_C:    {tOnC}"  .format(tOnC=PlugDevice.turnOnCmd_C))
print("turnOffCmd_C:   {tOffC}" .format(tOffC=PlugDevice.turnOffCmd_C))


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

zeroPower_reported = False
nrMeasurements = 0

filename = '/home/peter/repo/SmartPlugTools/te_arr_json2'

te_arr = []
te_arr = loadData(filename)

print('----------------------------')
print('----------------------------')
print('----------------------------')
print('te_arr = ', te_arr)
print('----------------------------')
print('----------------------------')
print('----------------------------')
while True:
  tMeasure    = time.time()
  ePlugDp = plugDrainpump.getPower()
  nrMeasurements = nrMeasurements + 1

  # Report non zero power or if zero hasn't been observed since before
  if (ePlugDp['Power'] > 0) or (zeroPower_reported == False):
    if (ePlugDp['Power'] == 0):
      zeroPower_reported = True
      sleepTime = 2.0

      saveData(filename, te_arr)
    else:
      zeroPower_reported = False
      sleepTime = 0.5

    te = {'Time' : tMeasure, 'Energy' : ePlugDp}
    te_arr.append(te)
    print("--------------------", nrMeasurements, "-----------------------")
    print("tMeasure         = ", tMeasure)
    print("ePlugDp          = ", ePlugDp)
    print("te               = ", te)
    print("Length of te_arr = ", len(te_arr))
    print("Size of te_arr   = ", sys.getsizeof(te_arr))
    print("te_arr           = ", te_arr)

  time.sleep(sleepTime)