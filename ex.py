from flask import Flask
from flask import request
from flask import jsonify
import json
import mysql.connector
from mysql.connector import errorcode



app = Flask(__name__)

DB_NAME = 'justIt'
userDB = 'root'
pswUserDB = '123456'
hostDB = '127.0.0.1'

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

    username = data.get("Username")

    cnx.cursor().execute("insert into utente(username,password,tipo) values('{}','{}',1);".format(username, data.get("Password")))
    cnx.cursor().execute("insert into ristorante(username,nome,categoria,indirizzo,aperto) values('{}','{}','{}','{}',false);".format(username, data.get("Nome"), data.get("Categoria"), data.get("Indirizzo")))
    cnx.commit()
    return jsonify(isError= False,
                    message= "Success",
                    statusCode= 200,
                    ), 200

@app.route('/insertClient', methods=["POST"])
def inserisciCliente():
    cnx = connectToDb()
    data = request.json

    username = data.get("Username");

    cnx.cursor().execute("insert into utente(username,password,tipo) values('{}','{}',0);".format(username, data.get("Password")))
    cnx.cursor().execute("insert into cliente(username,nome,cognome,indirizzo) values('{}','{}','{}','{}');".format(username, data.get("Nome"), data.get("Cognome"), data.get("Indirizzo")))
    cnx.commit()
    return jsonify(isError= False,
                    message= "Success",
                    statusCode= 200,
                    ), 200

@app.route('/searchUsername', methods=["GET"])
def controlloUsername():

    username = request.args.get('username')

    jsonResult = checkUsername(username)

    return jsonify(jsonResult)

@app.route('/searchUtente',methods=["GET"])
def controlloLogin():

    username = request.args.get('username')
    password = request.args.get('password')

    jsonResult = checklogin(username,password)

    #inserire sessione poi 

    return jsonify(jsonResult)
    
@app.route('/visualizzaRistoranti', methods=["GET"])
def visualizzaRistoranti():

    jsonResult = selectAllRestaurant();

    return jsonify(jsonResult);

@app.route('/openCloseRistorante', methods=["PUT"])
def openRistorante():
    cnx = connectToDb()
    data = request.json
    cursor = cnx.cursor()
    query = "update ristorante set aperto={} where username='{}'".format(data.get('aperto'), data.get('username'))
    cursor.execute(query)
    cnx.commit()
    return jsonify(isError= False,
                    message= "Success",
                    statusCode= 200,
                    ), 200

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0')