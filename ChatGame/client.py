#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk


def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tk.END, msg)
        except OSError:
            break


def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        frame.quit()


def on_closing():
    my_msg.set("{quit}")
    send()



frame = tk.Tk()
frame.title("Chat-Game")

messages_frame = tk.Frame(frame)
my_msg = tk.StringVar()
my_msg.set("Insert here your message.")
scrollbar = tk.Scrollbar(messages_frame)

msg_list = tk.Listbox(messages_frame, height=40, width=100, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tk.Entry(frame, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()

send_button = tk.Button(frame, text="Submit", command=send)
send_button.pack()


frame.protocol("WM_DELETE_WINDOW", on_closing)


HOST = "127.0.0.1"
PORT = 52001
if not PORT:
    PORT = 52001
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tk.mainloop()
