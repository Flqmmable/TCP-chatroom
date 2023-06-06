import socket
import threading
import time

clearScreen = "\n" * 50
roomOpen = True
waitingTime = 1
nickName = 'user1'


def join(ip, port):
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, int(port)))
    print(clearScreen)


def receiving():
    while roomOpen:
        msg = str(sock.recv(6000), 'utf-8')
        if msg == 'heartbeat':
            pass
        else:
            print(msg)


def send(message, nick):
    global sock
    sock.send(str.encode(f"{nick}: {message}"))


receiveThread = threading.Thread(target=receiving)

while True:
    print("Welcome to Chat Room!\n\n[1] Join a room\n[2] Exit\n")
    choice = input("Choice: ")

    if choice == '1':
        print(clearScreen)
        chatRoomIP = input("Enter chat room IP address: ")
        chatRoomPort = input("Enter chat room port: ")
        print(clearScreen)
        nickName = input("Enter a nickname: ")

        try:
            join(chatRoomIP, chatRoomPort)
        except socket.herror:
            print("Uh oh! Unable to join the chat room.")
            continue

        sock.send(str.encode(f"{nickName} has arrived!"))
        receiveThread.start()
        time.sleep(waitingTime)
        print(f"{nickName} has arrived!")

        while roomOpen:
            send(input(""), nickName)

    elif choice == '2':
        print("Goodbye!")
        exit()

    else:
        print("Invalid choice. Try again.")
        print(clearScreen)
