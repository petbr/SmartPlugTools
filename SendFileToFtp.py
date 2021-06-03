import sys
import ftplib

print ("Usage:      python3.5 <FTP site> <User> <Password>")
print('Argument List:', sys.argv)

ftpSite = sys.argv[1]
user = sys.argv[2]
password = sys.argv[3]
print("User=", user)
print("Password", password)

session = ftplib.FTP(ftpSite, user, password)
print("--")
session.dir()
print("--")
file = open('/var/log/DranpumpData/BeforeWater.html','rb')
ftpCommand = "STOR BeforeWater_ftpd.html";
print("Session storbinary")
ftpResponseMessage = session.storbinary(ftpCommand, file)
print("FtpCommand Response: ", ftpResponseMessage);
print("--")
session.dir()
print("--")
print("File close:")
file.close()
print("Session close")
session.close()



quit()
