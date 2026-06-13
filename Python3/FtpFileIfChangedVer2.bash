sajt="$1"
user="$2"
pwd="$3"
dirPath="$4"
filename="$5"

filenameWithPath="$dirPath$filename"

echo "Sajt: $sajt"
echo "User: $user"
echo "Pwd: $pwd"
echo "dirPath: $dirPath"
echo "filename: $filename"
echo "filenameWithPath: $filenameWithPath"
m1=""
echo $m1

#echo ---------- Starting FTP Thing >>  /var/log/DranpumpData/TheThing.log
#echo Start FTP  
#echo Start FTP  of $dirPath $filename >> /var/log/DranpumpData/TheThing.log

mlog1=""


while true; do
  # md5sum is computationally expensive, so check only once every 10 seconds
  sleep 60

  m2=$(md5sum "$filenameWithPath")
  #mlog2=$(md5sum /var/log/DranpumpData/TheThing.log)

  if [ "$m1" != "$m2" ] ; then
    #echo ---------- FTP Thing >> /var/log/DranpumpData/TheThing.log
    #date  >> /var/log/DranpumpData/TheThing.log
    date
    #echo FTP Sending new DATA file  >> /var/log/DranpumpData/TheThing.log
    echo $m2
    date
    date
    echo "Data file is changed, time to FTP file!"
    date
    date
    echo $m1
    m1=$m2
    python ../SendFileToFtp.py $sajt $user $pwd $dirPath $filename
  fi


  #if [ "$mlog1" != "$mlog2" ] ; then#
  #  echo $mlog2
  #  date
  #  date
  #  echo "Log file is changed, time to FTP file!"
  #  date
  #  date
  #  echo $mlog1
  #  mlog1=$mlog2
  #  python3.5 SendFileToFtp.py $sajt $user $pwd $dirPath "TheThing.log"
  #fi

  #python3.5 SendFileToFtp.py $sajt $user $pwd $dirPath "HEARTBEAT"

done
