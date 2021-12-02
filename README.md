# JustIt

# Inizializzazione Database

Il primo passaggio da effettuare riguarda l'installazione della libreria mySQL connector/python, una libreria che permette di far interagire il programma scritto in python con un database mySQL.

Questa può essere reperita al link: https://dev.mysql.com/downloads/connector/python/

Mediante mySQL Workbench, è necessario creare una nuova connessione avente i seguenti parametri:
  - Hostname: 127.0.0.1;
  - Port: 3306;
  - Username: root;
  - Connection Method: Standard(TCP/IP).

Successivamente aprire ed avviare il file: CreateDatabase.sql, così da creare il database con tutte le classi necessarie per il corretto funzionamento.

# Inizializzazione Server

- Installare Python per Windows mediante il link: https://www.python.org/downloads/
- Aprire una PowerShell nella directory: Progetto_APL_SERVER ed inserire i seguenti comandi:
  - py -m venv venv
  - venv\Scripts\activate, utile per avviare un ambiente venv
  - pip install flask
  - $env:FLASH_APP = "server.py"
  - python -m flask run

# Inizializzazione Client

Al fine di poter utilizzare l'API Web, sarà necessario installare i pacchetti NuGet:
- Microsoft.AspNet.WebApi.client
- Newtonsoft.Json (Framework JSON)

Questo potrà essere effettuando digitando: Install‐Package Microsoft.AspNet.WebApi.Client nella console di gestione pacchetti (PMC) che si al seguente percorso: Strumenti -> Gestione pacchetti NuGet -> Console di Gestione Pacchetti.

Successivamente avviare il client da Visual Studio o dal file.exe presente nella cartella bin/Test/Progetto_APL_CLIENT.exe

Per verificare l'interazione tra le due diverse tipologie di utenti, basterà avviare due volte l'eseguibile.
