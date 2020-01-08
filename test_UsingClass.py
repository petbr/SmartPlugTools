#!/usr/bin/env python2
#
import time
import json
from datetime import datetime
from PlugDevice import PlugDevice




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




