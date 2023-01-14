#!/usr/bin/env python3
import socket
import select
import os
import time
import sys
# time.ctime()

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = int(sys.argv[1])
d = 1
flag = 0
first_connection_flag = 0
closed_connection_flag = 0

log_str = ''
check_str = ''

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]

clients = {}
users = ["Online users"]

print("listening on port: " + str(PORT))


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}


    except:
        return False


def log_this_shit_up(log_str):
    f = open("logs.txt", "a+")
    f.write("[" + time.ctime() + "]" + log_str)
    log_str = ''
    f.close()


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket)

            if user is False:
                continue

            sockets_list.append(client_socket)

            clients[client_socket] = user

            if first_connection_flag == 0:
                print(
                    f"Accepted new connection from: {client_address[0]}:{client_address[1]} username: {user['data'].decode('utf-8')}")
                first_connection_flag = 1
                log_str += f"Accepted new connection from: {client_address[0]}:{client_address[1]} username: {user['data'].decode('utf-8')} \n"
                log_this_shit_up(log_str)
                log_str = ''
            else:
                first_connection_flag = 0

            if flag == 0:
                str1 = user['data'].decode('utf-8')
                if str1 != users[-1]:
                    users.append(str1)
        else:
            message = receive_message(notified_socket)

            if message is False:
                if closed_connection_flag == 0:
                    print(f"Closed connection from: {clients[notified_socket]['data'].decode('utf-8')}")
                    closed_connection_flag = 1
                    log_str += f"Closed connection from: {clients[notified_socket]['data'].decode('utf-8')} \n"
                    log_this_shit_up(log_str)
                    log_str = ''
                else:
                    closed_connection_flag = 0

                str1 = clients[notified_socket]['data'].decode('utf-8')
                sockets_list.remove(notified_socket)
                d = 0
                for i in users:
                    if i == str1:
                        users.pop(d)
                    d += 1

                del clients[notified_socket]
                continue

            user = clients[notified_socket]

            print(f"Received message from {user['data'].decode('utf-8')} : {message['data'].decode('utf-8')}")
            log_str += f"Received message from {user['data'].decode('utf-8')} : {message['data'].decode('utf-8')} \n"
            log_this_shit_up(log_str)
            log_str = ''
            # for i in users:
            #     print(i)
            for client_socket in clients:
                if client_socket != notified_socket:
                    y = str(users)
                    y = y.encode()
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'] + y)
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
