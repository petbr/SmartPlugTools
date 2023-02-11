import socket

# Server 

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = socket.socket(socket.AF_INET, socket.SO_REUSEADDR, 1)
s.bind(("192.168.1.7", 12345))

s.listen(10)
c, addr = s.accept()
print('{} connected.'.format(addr))

f = open("image.jpg", "rb")
datas = f.read(1024)

while datas:
    c.send(datas)
    datas = f.read(1024)

f.close()
s.close()
print("Done sending...")
