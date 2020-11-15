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

def client_program():
    (sHost, port, nrIters, printEach) = parseArgs()

    #host = socket.gethostname()  # as both code is running on same pc
    print("sHost = " + sHost)
    #host = "192.168.1.80"
    print("sHost = " + sHost)
    #port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((sHost, port))  # connect to the server

    #message = input(" -> ")  # take input
    message = "Start!"
    i = 0
    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response


        #message = input(" -> ")  # again take input
        message = "Kalle" + str(i)
        i = i + 1
        if i == nrIters:
            message = "bye"

    print('Sent to  server, number of calls: ' + str(i))  # show in terminal
    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
