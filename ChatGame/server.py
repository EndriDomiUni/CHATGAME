#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import game

""" accepts incoming connections """


def accepts_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("${0}: joined us.".format(client_address))
        client.send(bytes("Hello! Insert your name followed by the enter key !", "utf8"))

        indirizzi[client] = client_address
        Thread(target=manage_client, args=(client,)).start()


""" manage client and game """


def manage_client(client):
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you want leave chat, write {quit} or if you want to play write: {play}.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s joined us!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    # var to check a game phase
    phase = 0

    # var to check level/role of client
    level = 0
    roles = game.role[level]

    while True:
        msg = client.recv(BUFSIZ)

        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")

            if msg == bytes("{play}", "utf8"):

                # Ho provato a passare più variabili, nella speranza di far uscire le frasi con una andata a capo
                welcome_game = 'Benvenuto! Attualmento il ruolo è %s, \r\n' % roles
                info1 = 'Se vinci, aumenti di grado \r\n'
                info2 = 'altrimenti, lasci la stanza\r\n'
                client.send(bytes(welcome_game, "utf8"))
                client.send(bytes(info1, "utf8"))
                client.send(bytes(info2, "utf8"))

                intro = "Scegli un numero tra 1,2 o 3, ad esso sarà associata una domanda: \r\n"
                client.send(bytes(intro, "utf8"))

                phase = 1

            elif phase == 1:
                choice_quest = msg

                # get trap
                trap = game.get_trap()
                if choice_quest != bytes('1', "utf8") and choice_quest != bytes('2', "utf8") and choice_quest \
                        != bytes('3', "utf8"):
                    error = "Numero diverso da 1, 2 o 3. Riprova!\r\n"
                    client.send(bytes(error, "utf8"))
                else:
                    if choice_quest == bytes(str(trap), "utf8"):
                        client.send(bytes("Ops hai beccato la trappola \r\n", "utf8"))
                        broadcast(bytes("%s left the chat." % name, "utf8"))
                        client.send(bytes("{quit}", "utf8"))
                        client.close()
                        del clients[client]
                        break
                    else:
                        key_assigned, quest_assigned = game.assigns_quest()
                        client.send(bytes(quest_assigned, "utf8"))

                        phase = 2

            elif phase == 2:
                if game.check_answer(msg, key_assigned):
                    level += 1
                    actual_role = game.rank_role(level)
                    win = "Hai vinto"
                    client.send(bytes(win, "utf8"))

                    new_grade = "Il tuo nuovo grado è: %s \r\n" % actual_role
                    client.send(bytes(new_grade, "utf8"))

                    if win(actual_role):
                        say_goodbye = "HAI VINTO. FINE \r\n"
                        client.send(say_goodbye, "utf8")
                        client.send(bytes("{quit}", "utf8"))
                        client.close()
                        print("%s left the room", client)
                        del clients[client]
                        broadcast(bytes("%s left the chat." % name, "utf8"))
                        break

                    intro = "Scegli un numero tra 1,2 o 3, ad esso sarà associata una domanda: \r\n"
                    client.send(bytes(intro, "utf8"))

                    phase = 1
                else:
                    broadcast(bytes("%s wrong, Try Again!." % name, "utf8"))

        else:
            client.send(bytes("Ops hai beccato la trappola \r\n", "utf8"))
            client.send(bytes("{quit}", "utf8"))
            client.close()
            print("%s left the room", client)
            del clients[client]
            broadcast(bytes("%s left the chat." % name, "utf8"))
            break


""" update all clients """


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
