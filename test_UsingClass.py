#!/usr/bin/env python2
#
from PlugDevice import PlugDevice



print("Starting tester!")

plug1 = PlugDevice("Plug #1", "192.168.1.31")
plug3 = PlugDevice("Plug #3", "192.168.1.33")

# Class variables
print("Access port_C:  {ap}"    .format(ap=PlugDevice.accessPort_C))
print("Commands_C:     {cmds}"  .format(cmds=PlugDevice.commands_C))
print("timeCmd_C:      {timeC}" .format(timeC=PlugDevice.timeCmd_C))
print("powerCmd_C:     {pwrC}"  .format(pwrC=PlugDevice.powerCmd_C))
print("turnOnCmd_C:    {tOnC}"  .format(tOnC=PlugDevice.turnOnCmd_C))
print("turnOffCmd_C:   {tOffC}" .format(tOffC=PlugDevice.turnOffCmd_C))

# Instance variables plug1
print("Name:           {name}"  .format(name=plug1.name))
print("HostName:       {hostName}" .format(hostName=plug1.hostName))

# Instance variables plug3
print("Name:           {name}"  .format(name=plug3.name))
print("HostName:       {hostName}" .format(hostName=plug3.hostName))
