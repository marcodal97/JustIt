import threading
import socket
import time
import json

def login(client_socket):
        credenziali = client_socket.recv(1234)
        print(json.loads(credenziali.decode("utf-8")))
        

def client_thread(client_socket, address):
        print(f"Connessione da {address} accettata")
        client_socket.send(bytes("Connessione riuscita", "utf-8"))
        login(client_socket)
        

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(), 1234))
server_socket.listen(20)
clients = [server_socket]

while True:
	try:
                client_socket, address = server_socket.accept()
                clients.append(client_socket)
                threading.Thread(target=client_thread, args=(client_socket, address)).start()
	except:
                print("Closing server socket...")
                server_socket.close()
