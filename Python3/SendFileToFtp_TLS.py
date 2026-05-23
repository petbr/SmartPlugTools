import sys
from ftplib import FTP  # Vi importerar FTP direkt

print ("Usage:      python3.5 <FTP site> <User> <Password>")
print('Argument List:', sys.argv)

host     = sys.argv[1]
user     = sys.argv[2]
password = sys.argv[3]
dirPath  = sys.argv[4]
filename = sys.argv[5]

local_file = dirPath + "/" + filename

print("FTP site=    ", host)
print("User=        ", user)
print("Password=    ", password)
print("dirPath=     ", dirPath)
print("Filename=    ", filename)
print("FilenamePath=", local_file)



try:
    with FTP(host) as ftp:
        # Aktiverar debug för att se PASV-svaret i terminalen (valfritt)
        # ftp.set_debuglevel(2) 
        
        ftp.login(user=user, passwd=password)
        
        # Säkerställ passivt läge (True är standard, men bra att vara tydlig)
        ftp.set_pasv(True)
        
        print(f"Ansluten i passivt läge till {ftpSite}")

        with open(local_file, "rb") as f:
            # Vi skickar filen som en binär ström
            ftp.storbinary(f"STOR {filename}", f)
            
        print("Uppladdningen lyckades!")

except Exception as e:
    print(f"Ett fel uppstod: {e}")


print(f"Finished!")

exit
print(f"This will not be output!")
print(f"This will not be output!")
print(f"This will not be output!")
print(f"This will not be output!")
print(f"This will not be output!")
print(f"This will not be output!")


