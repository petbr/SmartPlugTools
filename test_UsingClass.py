#!/usr/bin/env python2
#
import time
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
print("Call Power Plug1:       {power}"   .format(power    = plug1.getPower()))
print("Call GetDateTime Plug1: {dt}"      .format(dt       = plug1.getDateTime()))
t1 = time.time()
# Instance variables plug2
print("------------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------------")
print("Name     #2:             {name}"    .format(name     = plug2.name))
print("HostName #2:             {hostName}".format(hostName = plug2.hostName))
print("Call Power Plug2:        {power}"   .format( power   = plug2.getPower()))
print("Call GetDateTime Plug2:  {dt}"      .format(dt       = plug2.getDateTime()))
t2 = time.time()

# Instance variables plug3
print("------------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------------")
print("Name     #3:             {name}"    .format(name     = plug3.name))
print("HostName #3:             {hostName}".format(hostName = plug3.hostName))
print("Call Power Plug3:        {power}"   .format( power   = plug3.getPower()))
print("Call GetDateTime Plug3:  {dt}"      .format(dt       = plug3.getDateTime()))
t3 = time.time()

# Instance variables Drainpump
print("------------------------------------------------------------------------------------")
print("------------------------------------------------------------------------------------")
print("Name             DrainPump:  {name}"    .format(name     = plugDrainpump.name))
print("HostName         DrainPump:  {hostName}".format(hostName = plugDrainpump.hostName))
print("Call Power       DrainPump:  {power}"   .format(power    = plugDrainpump.getPower()))
print("Call GetDateTime DrainPump:  {dt}"      .format(dt       = plugDrainpump.getDateTime()))
t_dp = time.time()

print("t1   = ", t1)
print("t2   = ", t2)
print("t3   = ", t3)
print("t_dp = ", t_dp)

dt1   = datetime.fromtimestamp(t1)
dt2   = datetime.fromtimestamp(t2)
dt3   = datetime.fromtimestamp(t3)
dt_dp = datetime.fromtimestamp(t_dp)

print("dt1   = ", dt1)
print("dt2   = ", dt2)
print("dt3   = ", dt3)
print("dt_dp = ", dt_dp)





