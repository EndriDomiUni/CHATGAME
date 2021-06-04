#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import senteces


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
    phase = 0
    level = 0

    while True:
        msg = client.recv(BUFSIZ)

        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")

            if msg == bytes("{play}", "utf8"):

                actual_role = senteces.role[level]
                welcome_game = 'Welcome to the game! Your actually role is %s,' % actual_role
                info1 = 'if you win: you rank up!'
                info2 = 'I will propose you three questions,'
                info3 = 'one will be a trick and you will lose the game immediately,'
                info4 = 'instead the other two contain a question'

                space = '\n'

                client.send(bytes(welcome_game, "utf8"))
                client.send(bytes(info1, "utf8"))
                client.send(bytes(info2, "utf8"))
                client.send(bytes(info3, "utf8"))
                client.send(bytes(info4, "utf8"))
                client.send(bytes(space, "utf8"))

                intro = "Scegli un numero tra 1,2 o 3, ad esso sarà associata una domanda:"
                client.send(bytes(intro, "utf8"))

                phase = 1
            elif phase == 1:
                choise_quest = msg
                print(choise_quest)
                trap = senteces.get_trap()

                print(trap)

                if choise_quest != bytes('1', "utf8") and choise_quest != bytes('2', "utf8") and choise_quest \
                        != bytes('3', "utf8"):
                    error = "Numero diverso da 1, 2 o 3. Riprova!"
                    client.send(bytes(error, "utf8"))
                else:
                    if choise_quest == bytes(str(trap), "utf8"):
                        broadcast(bytes("%s left the chat." % name, "utf8"))
                        client.send(bytes("{quit}", "utf8"))
                        client.close()
                        del clients[client]
                        break
                    else:
                        key_assigned, quest_assigned = senteces.assigns_quest()
                        client.send(bytes(quest_assigned, "utf8"))
                        phase = 2
            elif phase == 2:
                if senteces.check_answer(msg, key_assigned):
                    level += 1
                    client.send(bytes("You Win", "utf8"))
                    intro = "Scegli un numero tra 1,2 o 3, ad esso sarà associata una domanda:"
                    client.send(bytes(intro, "utf8"))
                    phase = 1
                else:
                    broadcast(bytes("%s wrong, Try Again!." % name, "utf8"))

        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            print("%s left the room", client)
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
