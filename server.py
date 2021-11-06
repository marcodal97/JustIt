from flask import Flask
from flask import request
from flask import jsonify
import json
import mysql.connector
from mysql.connector import errorcode
from mysql.connector.connection import MySQLConnection

app = Flask(__name__)

#DB_NAME = 'justIt'
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
def totalePietanze(cursor, lista):
    totale = 0
    for pietanza in lista:
        cursor.execute('select prezzo from pietanza where id = {}'.format(pietanza))
        res = cursor.fetchall()
        for row in res:
            totale = totale + row[0]  
    return totale

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

def createResult(isError, message, statusCode):
    jsonResult = []

    if message == '0':
        messageSend = 'Client'
    elif message == '1' :
        messageSend = 'Restaurant'
    else:
        messageSend = message
    
    jsonResult.append({
            'IsError' : isError,
            'Message' : messageSend,
            'StatusCode' : statusCode
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
        return jsonify(createResult(True, "Errore di connessione al database", 400))
        #return jsonify(isError= True,
         #           message= "Errore",
          #          statusCode= 400,
           #         )
    if not res:
        return jsonify(createResult(False, "Non Presente", 200))
        #return jsonify(isError= False,  
         #           message= "Non Presente",
          #          statusCode= 200,
           #         )
    else: 
        return jsonify(createResult(False, "Presente", 200))
            #return jsonify(isError= False,
             #       message= "Presente",
              #      statusCode= 200,
               #     )

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
        #return jsonify(isError= True,   #Se i dati sono errati il messaggio che invia al client è "Errati". Altrimenti invia il tipo dell'utente che si è loggato
        #            message= "Errore",
        #           statusCode= 400,
        #           )
        return jsonify(createResult(True, "Errore", 400))
    if not res:
        return jsonify(createResult(False, "Errati", 200))
        #return jsonify(isError= False,  
         #           message= "Errati",
          #          statusCode= 200,
           #         )
    else:
        if username in session:
            return jsonify(createResult(False, "Già loggato", 200))
            #return jsonify(isError= False,  
             #       message= "Già loggato",
              #      statusCode= 200,
               #     )
        session.append(username)
        print(session)
        for row in res:
            return jsonify(createResult(False, str(row[2]), 200))
            #return jsonify(isError= False,  
              #          message= row[2],
               #         statusCode= 200,
                #        )

@app.route('/logout', methods=["GET"])  
def logout():
    username = request.args.get('username')
    if session:
        if username in session:
            session.remove(username)
            return jsonify(createResult(False, "Success", 200))
            #return jsonify(isError=False,
             #               message= "Success",
              #              statusCode=200,
               #             )
    else: return jsonify(True, "Error", 400); 
        #return jsonify(isError= True,
         #           message= "Errore",
          #          statusCode= 400,
           #         )
    
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

@app.route('/menu', methods=['POST', 'GET', 'DELETE'])
def menu():
    cnx = connectToDb()
    cursor = cnx.cursor()
    match request.method:
        case 'POST':  #Inserimento menu
            data = request.json
            try:
                query = "insert into menu(username_ristorante, categoria) values ('{}','{}')".format(data.get('username_ristorante'), data.get('categoria'))
                cursor.execute(query)
                cnx.commit()
                query = "select LAST_INSERT_ID();"
                cursor.execute(query)
                res = cursor.fetchall()
            except mysql.connector.Error:
                return jsonify(isError= True,
                    message= "Errore richiesta",
                    statusCode= 400,
                    )
            for row in res:
                id = row[0]
            return jsonify(isError= str(False),
                            message= "Success",
                            statusCode= str(200),
                            id_m = str(id)
                            )
        case 'GET': #Restituisce informazioni base di un menu
            user = request.args.get('username_ristorante')
            try:
                cursor.execute("select * from menu where username_ristorante = '{}'".format(user)) 
                res = cursor.fetchall()
            except mysql.connector.Error:
                    return jsonify(isError= True,
                        message= "Errore richiesta",
                        statusCode= 400,
                        )
            jsonResult = []
            for row in res:
                jsonResult.append({
                    'id': row[0],
                    'username_ristorante': row[1],
                    'categoria': row[2]
                    })
            return jsonify(jsonResult)

        case 'DELETE':  #cancellazione menu
            id = request.args.get('id_menu')
            try:
                cursor.execute("delete from menu where id = {}".format(id)) 
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

@app.route('/pietanza', methods=['POST', 'GET', 'DELETE'])
def pietanza():
    cnx = connectToDb()
    cursor = cnx.cursor()
    match request.method:
        case 'POST':  #Inserimento pietanza
            data = request.json
            try:
                query = "insert into pietanza(id_menu,nome,descrizione,categoria,prezzo) values ('{}','{}','{}','{}',{})".format(data.get('id_menu'), data.get('nome'), data.get('descrizione'), data.get('categoria'),data.get('prezzo'))
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
        case 'GET':  #restituisce tutte le pietanze di un menu
            menu = request.args.get('id_menu')
            try:
                cursor.execute("select * from pietanza where id_menu = '{}'".format(menu)) 
                res = cursor.fetchall()
            except mysql.connector.Error:
                    return jsonify(isError= True,
                        message= "Errore richiesta",
                        statusCode= 400,
                        )
            jsonResult = []
            for row in res:
                jsonResult.append({
                    'id': row[0],
                    'id_menu': row[1],
                    'nome': row[2],
                    'descrizione': row[3],
                    'categoria': row[4],
                    'prezzo' : row[5]
                    })
            return jsonify(jsonResult)

        case 'DELETE': #cancellazione pietanza
            id = request.args.get('id_pietanza')
            try:
                cursor.execute("delete from pietanza where id = {}".format(id)) 
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

@app.route('/ordine', methods=['POST', 'GET'])
def ordine():
    cnx = connectToDb()
    cursor = cnx.cursor()
    match request.method:
        case 'POST': #Inserimento ordine
            data = request.json
            try:
                cursor.execute("insert into ordine(username_ristorante, username_utente, stato, totale) values('{}','{}','in attesa', 0)".format(data.get('username_ristorante'), data.get('username_utente')))
                cnx.commit()
            except mysql.connector.Error as err:
                return jsonify(isError= True,
                    message= "Errore richiesta",
                    cod_err = err.msg,
                    statusCode= 400,
                    )
            return jsonify(isError= False,
                            message= "Success",
                            statusCode= 200,
                            )
        case 'GET':  #restituisce le informazioni base di un ordine
            ordine = request.args.get('id_ordine')
            try:
                cursor.execute("select * from ordine where id = '{}'".format(ordine)) 
                res = cursor.fetchall()
            except mysql.connector.Error:
                    return jsonify(isError= True,
                        message= "Errore richiesta",
                        statusCode= 400,
                        )
            jsonResult = []
            for row in res:
                jsonResult.append({
                    'id': row[0],
                    'username_ristorante': row[1],
                    'username_utente': row[2],
                    'stato': row[3]                   
                    })
            return jsonify(jsonResult)

@app.route('/ordine_pietanza', methods=['GET','POST'])
def ordinePietanza():
    cnx = connectToDb()
    cursor = cnx.cursor()
    match request.method:
        case 'POST': #inserimento pietanze in un ordine
            data = request.json
            lista=data.get('lista_pietanze')
            totale=totalePietanze(cursor, lista)
            try:
                for pietanza in lista:
                    cursor.execute("insert into ordine_pietanza(id_ordine, id_pietanza) values('{}',{})". format(data.get('id_ordine'), pietanza))
                cursor.execute("update ordine set totale = {} where id = {}".format(totale, data.get('id_ordine')))
                cnx.commit()            
            except mysql.connector.Error as err:
                return jsonify(isError= True,
                    message= "Errore richiesta",
                    cod_err = err.msg,
                    statusCode= 400,
                    )
            return jsonify(isError= False,
                            message= "Success",
                            statusCode= 200,
                            )
        case 'GET':  #restituisce le pietanze di un ordine
            ordine = request.args.get('id_ordine')
            try:
                cursor.execute("select id_ordine, id_pietanza, id_menu, descrizione, categoria, prezzo from ordine_pietanza join pietanza on id_pietanza = id where id_ordine = {}".format(ordine))
                res = cursor.fetchall()
            except mysql.connector.Error as err:
                    return jsonify(isError= True,
                        message= "Errore richiesta",
                        cod_err = err.msg,
                        statusCode= 400,
                        )
            jsonResult = []
            #jsonResult.append({'id_ordine':ordine})
            for row in res:
                jsonResult.append({
                    'id_ordine':row[0],
                    'id_pietanza': row[1],
                    'id_menu': row[2],
                    'descrizione': row[3],
                    'categoria': row[4],
                    'prezzo': row[5]                   
                    })
            return jsonify(jsonResult)
 
@app.route('/statoOrdine', methods=['GET', 'POST'])
def statoOrdine():
    cnx = connectToDb()
    cursor = cnx.cursor()
    ordine = request.args.get('id_ordine')
    match request.method:
        case 'GET':
            try:
                cursor.execute("select stato from ordine where id = {}".format(ordine))
                res = cursor.fetchall()
            except mysql.connector.Error as err:
                    return jsonify(isError= True,
                        message= "Errore richiesta",
                        cod_err = err.msg,
                        statusCode= 400,
                        )
            jsonResult = []
            for row in res:
                jsonResult.append({
                    'stato_ordine':row[0]                   
                    })
            return jsonify(jsonResult)    
        case 'POST':
            data = request.json
            try:
                cursor.execute("update ordine set stato = '{}' where id = {}".format(data.get('stato'), data.get('id_ordine')))
                cnx.commit()            
            except mysql.connector.Error as err:
                return jsonify(isError= True,
                    message= "Errore richiesta",
                    cod_err = err.msg,
                    statusCode= 400,
                    )
            return jsonify(isError= False,
                            message= "Success",
                            statusCode= 200,
                            )



if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0')