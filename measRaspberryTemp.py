import os
import time

def measure_temp():
        temp = os.popen("vcgencmd measure_temp").readline()
	temp = temp.replace("temp=","")
	temp = temp.replace("'C","")
	return float(temp)

maxT = 0
minT = 100
while True:
        t = measure_temp()
	maxT = max(maxT, t)
	minT = min(minT, t)
	s = "t = " + str(t) + ", "
	s = s + "minT = " + str(minT) + ", "
	s = s + "maxT = " + str(maxT)
	print s

        time.sleep(5)