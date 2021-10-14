from flask import Flask
#from flask import request
#from flask_restful import Resource, Api
import json
from flask import jsonify
from flask import request





#from flask import Flask
#from flask import request
#from flask_restful import Resource, Api
#from flask import send_file
#from flask import jsonify
#import logging
#import json


app = Flask(__name__)

#api = Api(app)

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
    
if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0')
