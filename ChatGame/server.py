#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import senteces
import random


def accepts_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("${0}: joined us.".format(client_address))
        client.send(bytes("Hello! Insert your name followed by the enter key !", "utf8"))

        indirizzi[client] = client_address
        Thread(target=manage_client, args=(client,)).start()


def manage_client(client):
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you want leave chat, write {quit} or if you want to play write: {play}.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s joined us!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)

        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")

            if msg == bytes("{play}", "utf8"):

                actual_role = senteces.role[senteces.level]
                welcome_game = 'Welcome to the game! Your actually role is %s, if you win: you rank up! ' \
                               'I will propose you three questions, one will be a trick and you will lose the game ' \
                               'immediately' \
                               ', instead the other two contain a question' % actual_role

                # mandare messaggio: welcome_home
                client.send(bytes(welcome_game, "utf8"))

                # poni domande
                intro = "These are the three questions:"
                client.send(bytes(intro, "utf8"))

                quest1 = senteces.quest.get(random.randint(1, 8))
                quest2 = senteces.quest.get(random.randint(1, 8))
                trap = senteces.quest.get(random.randint(1, 8))

                # stampa quesiti
                client.send(bytes(quest1), "utf8")
                client.send(bytes(quest2), "utf8")
                client.send(bytes(trap), "utf8")

                # ottieni risposta
                answer = ""
                # se la risposta è uguale a trap -> quit

                # trap.value
                if answer == trap:
                    client.send(bytes("{quit}", "utf8"))
                    client.close()
                    del clients[client]
                    broadcast(bytes("%s left the chat." % name, "utf8"))
                    break
                # se la risposta è giusta -> rank up
                else:
                    senteces.rank_up(actual_role)
                    new_lever = "Your new role is %s" % actual_role
                    client.send(new_lever, "utf8")

                    # se il lvl è al max -> win
                    if actual_role == senteces.role["king"]:
                        win = "You have win %s" % name
                        client.send(bytes(win, "utf8"))

                # da capo
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
PORT = 52001
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for other connections...")
    ACCEPT_THREAD = Thread(target=accepts_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
