from flask import Flask
from flask import request
from flask import jsonify
import json
import mysql.connector
from mysql.connector import errorcode



app = Flask(__name__)

DB_NAME = 'db'
userDB = 'root'
pswUserDB = '123456'
hostDB = '127.0.0.1'

session = []

#api = Api(app)

def connectToDb():
    cnx = mysql.connector.connect(user = userDB, password = pswUserDB, host = hostDB)
    mySQLcursor = cnx.cursor()
    try:
        mySQLcursor.execute("use {};".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Il database non esiste, bisogna crearlo!")
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            mySQLcursor.execute("use {};".format(DB_NAME))
    return cnx

'''
def checklogin(username, password):
    cnx = connectToDb()
    cursor = cnx.cursor()
    query = "select * from utente where username='{}' and password='{}'".format(username,password)
    cursor.execute(query)
    res = cursor.fetchall()
    jsonResult = []
    for row in res:
        jsonResult.append({
            'Username':row[0],
            'Password':row[1],
            'Tipo':row[2]
            })
    return jsonResult
'''


'''
def checkUsername(username):
   cnx = connectToDb()
   cursor = cnx.cursor()
   query = "select * from utente where username='{}'".format(username)
   cursor.execute(query)
   res = cursor.fetchall()
   jsonResult = []
   for row in res:
       jsonResult.append({
            'Username':row[0],
            'Password':row[1],
            'Tipo':row[2]
            })
   return jsonResult
'''


def selectAllRestaurant():
   cnx = connectToDb()
   cursor = cnx.cursor()
   query = "select * from ristorante"
   cursor.execute(query)
   res = cursor.fetchall()
   jsonResult = []
   for row in res:
       jsonResult.append({
           'Username': row[0],
           'Nome': row[1],
           'Categoria': row[2],
           'Indirizzo': row[3],
           'Aperto': bool(row[4])
           })
   return jsonResult

@app.route('/insertRistorante', methods=["POST"])
def inserisciRistorante():
    cnx = connectToDb()
    data = request.json

    try:
        cnx.cursor().execute("insert into utente(username,pass,tipo) values('{}','{}',1);".format(data.get("Username"), data.get("Password")))
        cnx.cursor().execute("insert into ristorante(username,nome,categoria,indirizzo, aperto) values('{}','{}','{}','{}', false);".format(data.get("Username"), data.get("Nome_Ristorante"), data.get("Categoria"), data.get("Indirizzo")))
        cnx.commit()
    except mysql.connector.Error: 
        return jsonify(isError= True,
                    message= "Errore inserimento",
                    statusCode=400
                    )
    return jsonify(isError= False,
                    message= "Success",
                    statusCode= 200,
                    )

@app.route('/insertClient', methods=["POST"])
def inserisciCliente():
    cnx = connectToDb()
    data = request.json
    try:
        cnx.cursor().execute("insert into utente(username,pass,tipo) values('{}','{}',0);".format(data.get("Username"), data.get("Password")))
        cnx.cursor().execute("insert into cliente(username,nome,cognome,indirizzo) values('{}','{}','{}','{}');".format(data.get("Username"), data.get("Nome"), data.get("Cognome"), data.get("Indirizzo")))
        cnx.commit()
    except mysql.connector.Error:
        return jsonify(isError= True,
                        message= "Errore inserimento",
                        statusCode= 400,
                        )
    return jsonify(isError= False,
                    message= "Success",
                    statusCode= 200,
                    )

'''
@app.route('/searchUsername', methods=["GET"])
def controlloUsername():

    username = request.args.get('username')

    jsonResult = checkUsername(username)

    return jsonify(jsonResult)

'''

@app.route('/verificaUsername', methods=["GET"]) #per la registrazione
def verificaUsername():
    username = request.args.get('username')
    cnx = connectToDb()
    cursor = cnx.cursor()
    try:
        cursor.execute("select * from utente where username = '{}'".format(username))  #evita che un errore nella richiesta al database mi faccia bloccare il server
        res = cursor.fetchall()
    except mysql.connector.Error:
        return jsonify(isError= True,
                    message= "Errore",
                    statusCode= 400,
                    )
    if not res:
        return jsonify(isError= False,  
                    message= "Non Presente",
                    statusCode= 200,
                    )
    else: 
            return jsonify(isError= False,
                    message= "Presente",
                    statusCode= 200,
                    )


@app.route('/login',methods=["GET"])
def login():

    username = request.args.get('username')
    password = request.args.get('password')

    cnx = connectToDb()
    cursor = cnx.cursor()
    query = "select * from utente where username='{}' and pass='{}'".format(username,password)
    try:
        cursor.execute(query)
        res = cursor.fetchall()
    except mysql.connector.Error:       #Se c'è un errore di database isError = True altrimenti è False. 
        return jsonify(isError= True,   #Se i dati sono errati il messaggio che invia al client è "Errati". Altrimenti invia il tipo dell'utente che si è loggato
                    message= "Errore",
                    statusCode= 400,
                    )
    if not res:
        return jsonify(isError= False,  
                    message= "Errati",
                    statusCode= 200,
                    )
    else:
        if username in session:
            return jsonify(isError= False,  
                    message= "Già loggato",
                    statusCode= 200,
                    )
        session.append(username)
        print(session)
        for row in res:
            return jsonify(isError= False,  
                        message= row[2],
                        statusCode= 200,
                        )


@app.route('/logout', methods=["GET"])  
def logout():
    username = request.args.get('username')
    if session:
        if username in session:
            session.remove(username)
            return jsonify(isError=False,
                            message= "Success",
                            statusCode=200,
                            )
    else: return jsonify(isError= True,
                    message= "Errore",
                    statusCode= 400,
                    )
    
@app.route('/visualizzaRistoranti', methods=["GET"])
def visualizzaRistoranti():
    jsonResult = selectAllRestaurant()
    return jsonify(jsonResult)

@app.route('/openCloseRistorante', methods=["PUT"])
def openRistorante():
    cnx = connectToDb()
    data = request.json
    cursor = cnx.cursor()
    try:
        query = "update ristorante set aperto={} where username='{}'".format(data.get('aperto'), data.get('username'))
        cursor.execute(query)
        cnx.commit()
    except mysql.connector.Error:
        return jsonify(isError= True,
                    message= "Errore richiesta",
                    statusCode= 400,
                    )
    return jsonify(isError= False,
                    message= "Success",
                    statusCode= 200,
                    )






if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0')
