import sys
import ftplib

print ("Usage:      python3.5 <FTP site> <User> <Password>")
print('Argument List:', sys.argv)

ftpSite  = sys.argv[1]
user     = sys.argv[2]
password = sys.argv[3]
dirPath  = sys.argv[4]
filename = sys.argv[5]

filenamePath = dirPath + "/" + filename

print("FTP site=    ", ftpSite)
print("User=        ", user)
print("Password=    ", password)
print("dirPath=     ", dirPath)
print("Filename=    ", filename)
print("FilenamePath=", filenamePath)



session = ftplib.FTP(ftpSite, user, password)
print("--")
session.dir()
print("--")
file = open(filenamePath,'rb')
ftpCommand = "STOR " + filename
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
