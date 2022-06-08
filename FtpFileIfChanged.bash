filename="$1"
sajt="$2"
user="$3"
pwd="$4"
echo Sajt: $sajt
echo "User: $user"
echo "Pwd: $pwd"
m1=""
echo $m1

echo ---------- Starting FTP Thing >> /var/log/DranpumpData/TheThing.log
date  >> /var/log/DranpumpData/TheThing.log
echo Start FTP  >> /var/log/DranpumpData/TheThing.log

mlog1=""

while true; do
  # md5sum is computationally expensive, so check only once every 10 seconds
  sleep 20

  m2=$(md5sum "$filename")
  mlog2=$(md5sum /var/log/DranpumpData/TheThing.log)

  if [ "$m1" != "$m2" ] ; then
    echo ---------- FTP Thing >> /var/log/DranpumpData/TheThing.log
    date  >> /var/log/DranpumpData/TheThing.log
    echo FTP Sending new DATA file  >> /var/log/DranpumpData/TheThing.log

    echo $m2
    date
    date
    echo "Data file is changed, time to FTP file!"
    date
    date
    echo $m1
    m1=$m2
    python3.5 SendFileToFtp.py $sajt $user $pwd
  fi


  if [ "$mlog1" != "$mlog2" ] ; then
    echo $mlog2
    date
    date
    echo "Log file is changed, time to FTP file!"
    date
    date
    echo $mlog1
    mlog1=$mlog2
    python3.5 SendLogToFtp.py $sajt $user $pwd
  fi

done
