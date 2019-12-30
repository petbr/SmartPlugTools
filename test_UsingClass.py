#!/usr/bin/env python2
#
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

# Instance variables Drainpump
print("Name             DrainPump:  {name}"    .format(name     = plugDrainpump.name))
print("HostName         DrainPump:  {hostName}".format(hostName = plugDrainpump.hostName))
print("Call Power       DrainPump:  {power}"   .format(power    = plugDrainpump.getPower()))
print("Call GetDateTime DrainPump:  {dt}"      .format(dt       = plugDrainpump.getDateTime()))

# Instance variables plug1
print("Name     #1:      {name}"  .format(name=plug1.name))
print("HostName #1:      {hostName}" .format(hostName=plug1.hostName))
print("Call Power Plug1: {power}"   .format(power    = plug1.getPower()))

# Instance variables plug3
print("Name     #3:    {name}"  .format(name=plug3.name))
print("HostName #3:    {hostName}" .format(hostName=plug3.hostName))
print("Call Power Plug3: {power}"   .format( power=plug3.getPower()))

# Instance variables plug2
print("Name     #2:      {name}"  .format(name=plug2.name))
print("HostName #2:      {hostName}" .format(hostName=plug2.hostName))
print("Call Power Plug2: {power}"   .format( power=plug2.getPower()))






