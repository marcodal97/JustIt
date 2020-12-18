import threading
import socket
import time
import json

def cliente(client_socket):
        

def ristorante(client_socket):
        

def verifica_credenziali(credenziali):
        
        #connessione database per login
        if credenziali["username"] == 'ciao':
                return 0
        else:
                return 1        

def registrazione():
        #connessione database per registrazione
        print("Registrazione")

def login(client_socket):
        credenziali = client_socket.recv(1234)
        cred = json.loads(credenziali.decode("utf-8"))
        
        if(cred["tipo"] == 'login'):               
                while 1:
                        conferma = verifica_credenziali(cred)
                        if conferma == 0:
                                client_socket.send(bytes("Ok", "utf-8"))
                                print("Login effettuato")
                                return 5
                        else:
                                client_socket.send(bytes("Errati", "utf-8"))
                                credenziali = client_socket.recv(1234)
                                cred = json.loads(credenziali.decode("utf-8"))
        if cred ["tipo"] == 'registrazione':
                registrazione(client_socket)
                return

def client_thread(client_socket, address):
        print(f"Connessione da {address} accettata")
        client_socket.send(bytes("Connessione riuscita", "utf-8"))
        tipo = login(client_socket)
        if tipo == 5:
                cliente(client_socket)
        else: ristorante(client_socket)
        
        

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
