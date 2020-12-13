import socket
import time
import threading
import json


def login(server_socket):
    msg = server_socket.recv(1234)
    print(msg.decode("utf-8"))
    print("Inserire username")
    username = input()
    print("inserire password")
    password = input()
    credenziali = [username, password]
    server_socket.send(bytes(json.dumps(credenziali), "utf-8"))
    


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((socket.gethostname(), 1234))

login(server_socket)  


    
