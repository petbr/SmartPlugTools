import socket


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    print("Host = " + host)
    host = "192.168.1.80"
    print("Host = " + host)
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    i = 0
    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response


        #message = input(" -> ")  # again take input
        message = "Kalle" + str(i)
        i = i + 1
        if i == 100000:
            message = "bye"

    print('Sent to  server, number of calls: ' + i)  # show in terminal
    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
