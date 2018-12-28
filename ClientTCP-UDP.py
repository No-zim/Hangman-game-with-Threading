from socket import *
import random


def Client(a, b):
    host = a  # '127.0.0.1'
    port = b  # 5000
    print('Creating TCP for client')
    s = socket(AF_INET, SOCK_STREAM)
    n = input("Enter your name:")
    s.settimeout(5)
    try:
        s.connect((host, port))
    except error:
        print("Caught exception error, cannot connect")

    s.sendto(n.encode('utf-8'), (host, port))
    data = s.recv(1024)
    print(data.decode('utf-8'))
    data2 = s.recv(1024)                            # the port number of the Server UDP

    print('Received Server-UDP Port number: ', data2)
    h = 'localhost'
    p = random.randint(12000, 24000)                # creating UDP for yourself

    print('Creating UDP for Client')
    u = socket(AF_INET, SOCK_DGRAM)
    server = ('127.0.0.1', int(data2))              # address of Server UDP port

    u.bind((h, p))
    print("\nAre you ready kids?")

    while True:
        x = input("Enter: ready or start OR exit(to exit)):")
        if x == 'exit':
            u.sendto(x.encode('utf-8'), server)
            break

        u.sendto(x.encode('utf-8'), server)         # send 1
        inst, adds = u.recvfrom(2048)               # receive 2
        inst = inst.decode('utf-8')
        print('Instructions: ', inst)
        w, adds = u.recvfrom(1024)                  # 3 receive Word and number of guesses left
        w = w.decode('utf-8')
        print("Word: ", w[:len(w) - 2], " Guesses->", w[len(w) - 1])

        mess = input("guess <> OR end:")
        while True:
            if mess == 'end':
                u.sendto('end'.encode('utf-8'), server)
                break
            u.sendto(mess.encode('utf-8'), server)  # send 4 char
            count, adds = u.recvfrom(1024)
            count = count.decode('utf-8')
            res, adds = u.recvfrom(1024)            # 5 receive message back, first char is guess count
            r1 = res.decode('utf-8')
            print("Word: ", r1, " Guesses left->" + count)
            if r1[:3] == 'You':
                break
            mess = input("guess <>, end, exit:")
        if mess == 'end':
            c, adds = u.recvfrom(1024)
            d, adds = u.recvfrom(1024)
            print(d.decode('utf-8'), " Guesses left->", c.decode('utf-8'))
        print("\nARE YOU READY KIDS ?")

    u.sendto('bye'.encode('utf-8'), server)
    aws, adds = u.recvfrom(1024)
    print()
    print(aws.decode('utf-8'))
    print("Thank you for playing")


a = input("Enter Name of the server host ->localhost or 127.0.0.1: ")
b = int(input("Enter TCP Port number(it's 5000) for server process: "))
Client(a, b)
