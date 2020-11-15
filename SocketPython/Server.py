import socket
import sys

def parseArgs():
    sHost        = sys.argv[1]
    port         = int(sys.argv[2])
    nrIters      = int(sys.argv[3])
    printEachNth = int(sys.argv[4])
    print("F sHost      = ", sHost)
    print("F port      = ", port)
    print("F nrIters   = ", nrIters)
    print("F printEach = ", printEachNth)
    return (sHost, port, nrIters, printEachNth)

def server_program():
    (sHost, port, nrIters, printEach) = parseArgs()
    print("S sHost      = ", sHost)
    print("S port      = ", port)
    print("S nrIters   = ", nrIters)
    print("S printEach = ", printEach)

    # get the hostname
    #host = socket.gethostname()
    #host = "192.168.1.80"
    #port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((sHost, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    i = 0
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        # data = input(' -> ')
        data = "server answers: " + str(i)
        i = i + 1
        conn.send(data.encode())  # send data to the client

    print('Received from client, number of calls: ' + str(i))  # show in terminal
    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()