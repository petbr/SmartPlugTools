sajt="$1"
user="$2"
pwd="$3"
dirPath="$4"
filename1="$5"
filename2="$6"
filename3="BattPage.html"

filename1WithPath="$dirPath$filename1"
filename2WithPath="$dirPath$filename2"
filename3WithPath="$dirPath$filename3"

echo "Sajt: $sajt"
echo "User: $user"
echo "Pwd: $pwd"
echo "dirPath: $dirPath"
echo "filename1: $filename1"
echo "filename2: $filename2"
echo "filename3: $filename3"
echo "filename1WithPath: $filename1WithPath"
echo "filename2WithPath: $filename2WithPath"
echo "filename3WithPath: $filename3WithPath"
m1_Old=""
m2_Old=""
m3_Old=""

#echo ---------- Starting FTP Thing >>  /var/log/DranpumpData/TheThing.log
#echo Start FTP  
#echo Start FTP  of $dirPath $filename >> /var/log/DranpumpData/TheThing.log



while true; do
  # md5sum is computationally expensive, so check only once every 10 seconds
  sleep 60

  m1_New=$(md5sum "$filename1WithPath")
  m2_New=$(md5sum "$filename2WithPath")
  m3_New=$(md5sum "$filename3WithPath")
  #mlog2=$(md5sum /var/log/DranpumpData/TheThing.log)

  if [ "$m1_New" != "$m1_Old" ] ; then
    #echo ---------- FTP Thing >> /var/log/DranpumpData/TheThing.log
    #date  >> /var/log/DranpumpData/TheThing.log
    date
    #echo FTP Sending new DATA file  >> /var/log/DranpumpData/TheThing.log
    date
    date
    echo "Data $filename1 is changed, time to FTP file!"
    date
    date
    m1_Old=$1_New
    python ../SendFileToFtp.py $sajt $user $pwd $dirPath $filename1
  fi

  if [ "$m2_New" != "$m2_Old" ] ; then
    #echo ---------- FTP Thing >> /var/log/DranpumpData/TheThing.log
    #date  >> /var/log/DranpumpData/TheThing.log
    date
    #echo FTP Sending new DATA file  >> /var/log/DranpumpData/TheThing.log
    date
    date
    echo "Data $filename2 is changed, time to FTP file!"
    date
    date
    m2_Old=$2_New
    python ../SendFileToFtp.py $sajt $user $pwd $dirPath $filename2
  fi

  if [ "$m3_New" != "$m3_Old" ] ; then
    #echo ---------- FTP Thing >> /var/log/DranpumpData/TheThing.log
    #date  >> /var/log/DranpumpData/TheThing.log
    date
    #echo FTP Sending new DATA file  >> /var/log/DranpumpData/TheThing.log
    date
    date
    echo "Data $filename3 is changed, time to FTP file!"
    date
    date
    m3_Old=$3_New
    python ../SendFileToFtp.py $sajt $user $pwd $dirPath $filename3
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
