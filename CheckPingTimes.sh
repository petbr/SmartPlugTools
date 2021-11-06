#!/bin/bash

echo "Arg1 = $1"

PingCoupleOfTimes () {
address1=$1
address2=$2
address3=$3
nrIters=$4

pResult=2
for ((i = 0; i < $nrIters ; i++)); do

  ping -c1 $address1 > /dev/null
  if [ $? == 0 ]; then
    echo "$address1 OK! in PingCoupleOfTimes! i=$i($nrIters), ERROR=$?"
    pResult=0
  else
    echo "$address1 FAILS in PingCoupleOfTimes! i=$i($nrIters), ERROR=$?"
    pResult=2
  fi

  ping -c1 $address2 > /dev/null
  if [ $? == 0 ]; then
    echo "$address2 OK! in PingCoupleOfTimes! i=$i($nrIters), ERROR=$?"
    pResult=0
  else
    echo "$address2 FAILS in PingCoupleOfTimes! i=$i($nrIters), ERROR=$?"
    pResult=2
  fi

  ping -c1 $address3 > /dev/null
  if [ $? == 0 ]; then
    echo "$address3 OK! in PingCoupleOfTimes! i=$i($nrIters), ERROR=$?"
    pResult=0
  else
    echo "$address3 FAILS in PingCoupleOfTimes! i=$i($nrIters), ERROR=$?"
    pResult=2
  fi

  sleep 5    

done
echo "PingCoupleOfTimes => $pResult"

return $pResult
}



while :
do

echo "\n"
echo "\n"
PingCoupleOfTimes 192.168.1.1 192.168.1.18 google.se 5
echo "PingCoupleOfTimes just replied: $?"
result=$?
if [ $result=0 ]; then
  date
  echo "WORKS!" > /dev/null
else
  date
  echo "FAILS!"
fi

sleep 1000

done










PingCoupleOfTimes 192.168.1.18 3
result=$?
echo "Result = $result"
if [ $result=0 ]; then
  echo "if.......IT WORKS!"
else
  echo "else.......IT doesnt WORK!"
fi
echo "After loop result = $result"



PingCoupleOfTimes 192.168.1.18 4
result=$?
echo "Result = $result"

if [ $result=0 ]; then
  echo "if.......IT WORKS!"
else
  echo "else.......IT doesnt WORK!"
fi
echo "After loop result = $result"
