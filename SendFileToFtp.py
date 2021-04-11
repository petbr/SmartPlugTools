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
print("#1")
session.dir()
session.mkd("Test")
print("#2")
session.dir()
session.rmd("Test")
print("#3, dir")
session.dir()
print("#3, file open")
file = open('/var/log/DranpumpData/BeforeWater.html','rb')
print("#5, session storbinary")

ftpCommand = "STOR BeforeWater_ftpd.html";
ftpResponseMessage = session.storbinary(ftpCommand, file)
print("ftpCommand Response: ", ftpResponseMessage);

print("#6, file close:")
file.close()
print("#7, session close")
session.close()



quit()
