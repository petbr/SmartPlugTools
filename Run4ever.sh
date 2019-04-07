#!/bin/bash
while true; do
  curTime=$(date "+%Y%m%d_%H%M%S")
  echo "Current Time: $curTime"
  newFileName=RestartIndicator_$curTime.txt
  echo "New FileName: "$newFileName
  
  sleep 5
  touch /tmp/DranpumpData/$newFileName
  python test.py -t 192.168.1.18 -c energy | tee /tmp/DranpumpData/ful_log.txt
done