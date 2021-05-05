#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accepts_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s: si è collegato." % client_address)
        client.send(bytes("Salve! Digita il tuo Nome seguito dal tasto Invio!", "utf8"))
        indirizzi[client] = client_address
        Thread(target=manage_client, args=(client,)).start()


def manage_client(client):
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Benvenuto %s! Se vuoi lasciare la Chat, scrivi {quit} per uscire.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s si è unito all chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):
    for user in clients:
        user.send(bytes(prefix, "utf8") + msg)


clients = {}
indirizzi = {}

HOST = ''
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("In attesa di connessioni...")
    ACCEPT_THREAD = Thread(target=accepts_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()