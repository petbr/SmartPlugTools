import os
import time

hostname = "google.com" #example
sleepTime = 1

lastResponse = os.system("ping -c 1 " + hostname + " > /dev/null")

lastTime = time.time();

print('************ Starting! **************')
print('************ Starting! **************')
print('************ Starting! **************')
print('************ Starting! **************')
while True:
  #and then check the response...
  response = os.system("ping -c 1 " + hostname + " > /dev/null")
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
        
        
