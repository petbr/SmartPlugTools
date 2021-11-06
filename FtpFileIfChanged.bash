filename="$1"
sajt="$2"
user="$3"
pwd="$4"
echo Sajt: $sajt
echo "User: $user"
echo "Pwd: $pwd"
m1=""
echo $m1



while true; do

  # md5sum is computationally expensive, so check only once every 10 seconds
  sleep 20

  m2=$(md5sum "$filename")

  if [ "$m1" != "$m2" ] ; then
    echo $m2
    date
    date
    echo "File is changed, time to FTP file!"
    date
    date
    echo $m1
    m1=$m2
    python3.5 SendFileToFtp.py $sajt $user $pwd
  fi
done
