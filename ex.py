from flask import Flask
from flask import request
from flask import jsonify
import json
import mysql.connector
from mysql.connector import errorcode





#from flask import Flask
#from flask import request
#from flask_restful import Resource, Api
#from flask import send_file
#from flask import jsonify
#import logging
#import json


app = Flask(__name__)

#api = Api(app)


DB_NAME = 'db'
userDB = 'root'
pswUserDB = '123456'
hostDB = 'localhost'

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
    if username == "user" and password == 'pass':
        return 'ok'
    else:
        return 'error'


@app.route('/registrazione',methods=["GET"])
def provametodo():
    return jsonify("provaAPI")

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
    jsonResult = []

    jsonResult.append({
        'Username':"ciao",
        'Password': "ciao"
    })
    return jsonify(jsonResult)

@app.route('/searchUtente',methods=["GET"])
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    res = checklogin(username,password)

    #inserire sessione poi 

    if res == 'ok':

        jsonResult = []

        jsonResult.append({
            'Username':"ciao",
            'Password': "ciao"
        })

        return jsonify(jsonResult)
        print("login effettuato")
    else:
        return jsonify(isError= True,
                    message= "Failed",
                    statusCode= 404,)
        print("errore login")
        
        
        
        
        
 @app.route('/visualizzautenti', methods=["GET"])
 def visualizaOrdini():
    cnx = connectToDb()
    cursor = cnx.cursor()
    cursor.execute("select * from utente")
    res = cursor.fetchall()
    for row in res:
        print("utente: {} - password: {} - tipo: {}".format(row[0],row[1],row[2]))
    return jsonify(isError= False,
                    message= "Success",
                    statusCode= 200,
                    )


    
if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0')
