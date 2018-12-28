from socket import *
import random
import _thread

udpPorts = []   # for list of UDP ports, in order to prevent collision


def new_client(c, addr, command):
    inst = "This is hangman You will guess one letter at a time. If the letter is in the hidden word the '-' will be\n" \
           "replaced by the correct letter Guessing multiple letters at a time will be considered as guessing the entire\n" \
           "word (which will result in either a win or loss automatically - win if correct, loss if incorrect).You win\n" \
           "if you either guess all of the correct letters or guess the word correctly. You lose if you run out of\n" \
           "attempts. Attempts will be decremented in the case of an incorrect or repeated letter guess.\n" \
           "Enter 'Start' or 'Exit' when you're asked 'Are you Ready?' " \
           "In the game you must enter 'guess <char>' to guess or 'end' to end the game\n"

    data = c.recv(1024).decode('utf-8')                             # received from client
    print("User's name is: ", data)
    r = "Hello " + data
    c.send(r.encode('utf-8'))
    # now udp-------------------------------------------------------

    h = '127.0.0.1'
    p = random.randint(5001, 12000)
    if p not in udpPorts:
        udpPorts.append(p)
    else:
        p = random.randint(5001, 12000)
    print("Creating UDP socket")
    u = socket(AF_INET, SOCK_DGRAM)
    u.bind((h, p))
    print("Sending UDP port number to client using TCP connection...")
    c.send(str(p).encode('utf-8'))
    print()
    words = []
    with open("words.txt", 'r') as file:                            # reads from the file and makes a list of words
        for line in file:
            line = line.strip()
            words.append(line)

    com, adds = u.recvfrom(1024)                                    # 1 receive
    com = com.decode('utf-8').lower()                               # receive 'start' message or 'exit'

    while com != 'exit':
        u.sendto(inst.encode('utf-8'), adds)                        # 2 send instructions
        random.shuffle(words)                                       # shuffle the list and take the first
        display = []
        if command == '-r':
            word = list(words[0])                                   # make it a list
        else:
            word = list(command)
        print('Hidden word: ', word)

        for i in range(len(word)):
            display.append('_')
        count = 0

        display = list(display)
        print('The game is on,guess')
        u.sendto((str(display) + str((len(word)+1) - count)).encode('utf-8'), adds)# 3 send words and count
        char, adds = u.recvfrom(1024)                                          # get a guess <>, or end. 4 Receive char

        while True and count < len(word)+1:
            print(char.decode('utf-8'))
            char = char.decode('utf-8').lower()
            count += 1
            if char[:3] == 'end':
                u.sendto(str((len(word)+1) - count).encode('utf-8'), adds)
                u.sendto(("You LOST! The word was " + str(word)).encode('utf-8'), adds)
                break
            elif len(char) > 7:   # it means you are trying to guess the entire word
                o = char[6:]
                print(o)
                if fun(word, o):
                    u.sendto(str((len(word)+1) - count).encode('utf-8'), adds)
                    u.sendto(("You got it!!! Bulls eye! the word is " + str(o)).encode('utf-8'), adds)
                    break
                else:
                    u.sendto(str((len(word)+1) - count).encode('utf-8'), adds)
                    u.sendto(("You LOST! The word was " + str(word)).encode('utf-8'), adds)
                    break
            elif char[:5] == 'guess':
                display = list(display)
                r = char[len(char) - 1]

                for i in range(len(word)):
                    if word[i] == r:
                        display[i] = r

                if display == word:
                    u.sendto(str((len(word)+1) - count).encode('utf-8'), adds)
                    u.sendto(("You got it!!! Bulls eye! the word is " + str(display)).encode('utf-8'), adds)
                    break
                else:
                    u.sendto(str((len(word)+1) - count).encode('utf-8'), adds)    # 5 send count
                    print('Sending display ', display)
                    u.sendto(str(display).encode('utf-8'), adds)                  # 6 send the word

            char, adds = u.recvfrom(1024)                                         # 7 Receive char again
        if display != word and count > len(word)+1:
            u.sendto(str((len(word)+1) - count).encode('utf-8'), adds)
            u.sendto(("You LOST! The word was " + str(word)).encode('utf-8'), adds)

        com, adds = u.recvfrom(1024)                                              # 8 Receive start or exit
        com = com.decode('utf-8')
        print("received com which is: ", com)
        if com == 'exit':
            break
    f, adds = u.recvfrom(1024)                                                    # 9 receive 'bye' message
    f = f.decode('utf-8')
    print(f)

    u.sendto("Closing UDP and TCP sockets...".encode('utf-8'), adds)              # 10 send end message
    u.close()


def Server(command):

    print("Server is on")

    host = 'localhost'
    port = 5000
    print('Creating TCP socket')
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((host, port))
    s.listen(10)
    print('TCP is on')

    while True:
        con, addr = s.accept()                                          # accept
        print("Huston, we have a connection" + str(addr))               # print the address we're connecting to
        _thread.start_new_thread(new_client, (con, addr, command))      # start a new thread

    s.close()                                                           # Close the TCP connection


def fun(word, string):              # first is the current word we are guessing, second is received guess string
    string = list(string)           # this function checks if a user makes a whole word guess
    for i in range(len(word)):
        if word[i] != string[i]:
            return False
    return True


a = input("Enter only '-r' (for random words) or any word:")
Server(a)
