import socket
import time
import threading
import json


def login(server_socket):
    msg = server_socket.recv(1234)
    print(msg.decode("utf-8"))
    print("1: login\n2: registrazione")
    tipo = int(input())
    if tipo == 1:
        while 1:
            print("Inserire username")
            username = input()
            print("inserire password")
            password = input()
            credenziali = {"username": username, "password": password, "tipo":"login"}
            server_socket.send(bytes(json.dumps(credenziali), "utf-8"))
            msg = server_socket.recv(1234)
            print(msg.decode("utf-8"))
            msg_d = msg.decode("utf-8")
            if msg_d == "Ok":
                print("login effettuato")
                return
    if tipo == 2:
        credenziali = {"tipo":["registrazione"]}
        print("registrazione")
    


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((socket.gethostname(), 1234))

login(server_socket)



    
