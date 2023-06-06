import socket
import threading
import art
import time
import re

chatRoomWelcome = art.text2art('Welcome\n\n', font='funface')
waitingTime = 1
clearScreen = "\n" * 50
clients = []
nickNames = []


def broadcast(msg):
    for c in clients:
        c.send(str.encode(msg))


def connectionChecking():
    while True:
        if len(clients) > 0:
            time.sleep(1)
            for cl in clients:
                try:
                    cl.send(str.encode('heartbeat'))
                except:
                    for cli in nickNames:
                        if cli['Connection'] == cl:
                            clients.remove(cl)
                            nickNames.remove(cli)
                            broadcast(cli["Nickname"] + " has left.")


def receive(connection):
    while True:
        try:
            msg = str(connection.recv(1024), 'utf-8')
            if ":" not in msg:
                match = re.search('^.+?\s', msg)
                nickNames.append({"Connection": connection, "Nickname": match.group(0).rstrip()})
            for c in clients:
                if c != connection:
                    c.send(str.encode(msg))
        except:
            pass


def host():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 3333))
    sock.listen()

    while True:
        conn, add = sock.accept()
        conn.send(str.encode(chatRoomWelcome))
        clients.append(conn)
        receiveThread = threading.Thread(target=receive, args=(conn,))
        receiveThread.start()


hostThread = threading.Thread(target=host)
checkThread = threading.Thread(target=connectionChecking)

input("Press enter to host chat room: ")
print(clearScreen)
print("Hosting a chat room on localhost:3333.")
time.sleep(waitingTime)
hostThread.start()
checkThread.start()
print("Chat room has been created on localhost:3333!")
