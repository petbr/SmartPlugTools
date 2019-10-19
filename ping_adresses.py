import os
import time
import sys

print("Num of args: ", len(sys.argv))
print("Arg lists: ", str(sys.argv))
print("Arg[1]: ", sys.argv[1])

hostname = sys.argv[1] #example
sleepTime = 1


lastResponse = os.system("ping -i 5 -c 1 " + hostname + " > /dev/null")

lastTime = time.time();

def pingExtraIfFailed(address, nrTries, delayBetweenTries):
  response = os.system("ping -i 5 -c 1 " + address + " > /dev/null")
  
  if ((response == 0) or (nrTries == 1)):
    return response

  time.sleep(delayBetweenTries)
  return pingExtraIfFailed(address, nrTries-1, delayBetweenTries)

print('************ Starting! **************')
print('************ Starting! **************')
print("IP pinging: " + hostname)
print('************ Starting! **************')
print('************ Starting! **************')
while True:
  #and then check the response...
#  response = os.system("ping -c 10 " + hostname + " > /dev/null")
  response = pingExtraIfFailed(hostname, 3, 1)
  localTime = time.localtime()
  nowTime = time.time();
  timeStr = time.strftime("%H:%M:%S", localTime)
  
  if response != lastResponse:
    print("")
    print(timeStr)
    print("Seconds since last state: " + str(nowTime - lastTime))
    lastTime = nowTime
    lastResponse = response;
    if response == 0:
      print(hostname, 'is up!')
    else:
      print(hostname, 'is down!')    
  time.sleep(sleepTime)
        
        
