import os
import json
import pandas as pd
import numpy as np
import sys
import traceback
import argparse

from random import randrange, randint
from flask import Flask, render_template, request

sys.path.append(os.path.abspath(os.path.join('..')))


app = Flask(__name__)


# Está rota serve para enviar uma frase e recebê-la de volta com algumas palavras trocadas por sinônimos:
@app.route("/message/synonyms", methods=['GET'])
def message_synonyms():
    web_service_return = {}
    
    try:        
        # Transforma os dados do formato json para um dicionário python:
        message = request.get_json()

        # TODO: processamento da mensagem e retorno

        web_service_return['message'] = None
        web_service_return['result'] = 'executado com sucesso' 

    except Exception as e:
        # Mostra o stack trace de erros:
        traceback.print_exc()
        web_service_return['message'] = None
        web_service_return['result'] = 'ocorreu o seguinte erro: ' + str(e)

    web_service_return_json = json.dumps(web_service_return)

    return web_service_return_json


# Essa rota serve para enviar uma frase e receber de volta a possível intenção (intent)
# que o cliente possuia ao enviá-la para o Chatbot:
@app.route("/message/intent/get", methods=['GET'])
def message_intent_get():
    web_service_return = {}
    
    try:        
        # Transforma os dados do formato json para um dicionário python:
        message = request.get_json()

        # TODO: processamento da mensagem e retorno da intent

        web_service_return['intent'] = None
        web_service_return['result'] = 'executado com sucesso' 

    except Exception as e:
        # Mostra o stack trace de erros:
        traceback.print_exc()
        web_service_return['intent'] = None
        web_service_return['result'] = 'ocorreu o seguinte erro: ' + str(e)

    web_service_return_json = json.dumps(web_service_return)

    return web_service_return_json


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--type", required=True, help="se a execução será feita como local ou não")
    ap.add_argument("-p", "--port", required=False, help="a porta do servidor", nargs='?', const=6600)
    ap.add_argument("-hs", "--host", required=False, help="o endereço de hospedagem do servidor", nargs='?', const="ec2-18-209-38-187.compute-1.amazonaws.com")

    args = vars(ap.parse_args())

    # Inicializa o servido da aplicação:
    if args["type"] == "test":
        app.run(debug=True)
    elif args["type"] == "production":
        app.run(debug=True, port=args["host"], host=args["port"])

