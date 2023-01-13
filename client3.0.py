import tkinter as tk
from tkinter import *
import threading
import socket
import errno
import sys
import time
import os 

global i, username, IP, message, clients
message = ''
IP = 1
i = 1
username = ''
clients = []


def start_EZ(event):
    global username, IP, PORT
    IP = f1_text.get()
    username = f2_text.get()
    PORT = f3_text.get()
    first_window.destroy()


def start_EZ2():
    global username, IP, PORT
    IP = f1_text.get()
    username = f2_text.get()
    PORT = f3_text.get()
    first_window.destroy()


first_window = tk.Tk()
first_window.title("startup")
first_window.geometry("400x400")
#first_window.eval('tk::PlaceWindow %s center' % first_window.winfo_pathname(first_window.winfo_id()))  ## if on linux you can activate this
first_window.configure(bg="lightgreen")
first_window.bind('<Return>', start_EZ)

f1_text = tk.Entry(first_window)
f1_text.insert(0, '127.0.0.1')
f2_text = tk.Entry(first_window)
f2_text.insert(1, 'username')
f3_text = tk.Entry(first_window)
f3_text.insert(1, 'port')
f1_text.pack()
f2_text.pack()
f3_text.pack()
first_button = Button(first_window, text="submit", bg="lightblue", command=start_EZ2)
first_button.pack()
first_window.mainloop()

# Main window


window = tk.Tk()
window.title("dvirsuppp")
window.geometry("1000x640")
#window.eval('tk::PlaceWindow %s center' % window.winfo_pathname(window.winfo_id()))   ## if on linux you can activate this
window.configure(bg="lightgreen")


def incom_message(usr, msg):
    my_text.configure(state=NORMAL)
    my_text.insert(END, usr + "( " + time.ctime() + ')' + " :" + msg + "\n")
    str2 = usr + "( " + time.ctime() + ')' + " :" + msg + "\n"
    os.system("echo" +  str2)
    my_text.configure(state=DISABLED)
    my_text.yview(END)


def click(event):
    message = textbox.get()
    message = message.encode("utf-8")
    message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
    client_socket.send(message_header + message)
    textbox.delete(0, 'end')
    online_users.delete(0, 'end')



def click2():
    message = textbox.get()
    message = message.encode("utf-8")
    message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
    client_socket.send(message_header + message)
    textbox.delete(0, 'end')
    online_users.delete(1.0, 'end')


window.bind('<Return>', click)

pane_1 = PanedWindow(window, bd=4, relief="raised", bg="lightblue")
pane_1.pack(fill=BOTH, expand=1)


pane_2 = PanedWindow(pane_1, bd=4, relief="raised", bg="lightgreen", height=20, width=20)
pane_2.place(x=140, y=0, height=500, width=850)
v = tk.Scrollbar(window)
v.pack(side=RIGHT, fill=Y)
my_text = Text(pane_2,  wrap=NONE, yscrollcommand=v.set)
my_text.configure(state=DISABLED)
my_text.pack(side=TOP, fill=X)
v.config(command=my_text.yview)
pane_2.add(my_text)

pane_3 = PanedWindow(pane_1, bd=4, relief="raised", bg="lightgreen")
pane_3.place(x=140, y=500, width=850, height=100)

pane_4 = PanedWindow(pane_1, bd=4, relief="raised", bg="lightgreen")
pane_4.place(x=850, y=515, width=130, height=70)

pane_5 = PanedWindow(pane_1, bd=4, relief="raised", bg="lightgreen")

pane_5.place(x=1, y=1, width=135, height=600)

online_users = Text(pane_5, wrap=NONE, yscrollcommand=v.set)
online_users.configure(state=DISABLED)
pane_5.add(online_users)

buttom = tk.Button(pane_4, text="send", bg="lightblue", command=click2)
pane_4.add(buttom)

textbox = tk.Entry(pane_3)
pane_3.add(textbox)


# textbox.place(x=100, y=450)

def users_list(str1):
    online_users.configure(state=NORMAL)
    online_users.delete(1.0, 'end')
    online_users.insert(END, str1)
    online_users.configure(state=DISABLED)



def lisener():
    global IP, message
    HEADER_LENGTH = 10
    PORT = 1233
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    client_socket.setblocking(False)

    username = my_username.encode("utf-8")
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
    client_socket.send(username_header + username)

    while True:
        try:
            while True:
                # receive things
                username_header = client_socket.recv(HEADER_LENGTH)
                if not len(username_header):
                    print("Connection closed by the server")
                    sys.exit()
                username_length = int(username_header.decode("utf-8").strip())
                username = client_socket.recv(username_length).decode('utf-8')

                message_header = client_socket.recv(HEADER_LENGTH)

                message_length = int(message_header.decode('utf-8').strip())
                message = client_socket.recv(message_length).decode('utf-8')
                on_users = client_socket.recv(4096).decode('utf8')
                on_users = on_users .replace('[', '', 1)
                on_users = on_users .replace(']', '', 1)
                on_users = on_users .replace(',', '\n', 100)
                users_list(on_users)
                incom_message(username, message)

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print("Reading error", str(e))
                sys.exit()
            continue


        except Exception as e:
            print('General error', str(e))
            sys.exit()


HEADER_LENGTH = 10
PORT = 1233
my_username = username
check = my_username
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

username = my_username.encode("utf-8")
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + username)

t1 = threading.Thread(target=lisener)
t1.start()

window_thread = threading.Thread(target=window.mainloop())
window_thread.start()
