from helper.openai_api import text_complition, entity_rec
from helper.twilio_api import send_message, send_welcome_message, get_f, set_f_to_false


from flask import Flask, request, session
from dotenv import load_dotenv
from loguru import logger
import os


import pandas as pd
import json
import numpy as np


load_dotenv()

secret_key = os.getenv("SECRET_KEY")

app = Flask(__name__)

app.config['SECRET_KEY'] = secret_key

@app.route('/')
def home():
    return 'All is well...'


@app.route('/twilio/receiveMessage', methods=['POST'])
def receiveMessage():

    # Getting information from Whatsapp

    profile_name = request.form['ProfileName']
    sender_id = request.form['From']
    wa_id = request.form['WaId']

    # Debuging the information

    logger.debug(f"User: {profile_name}")
    logger.debug(f"From: {sender_id}")

    # Getting user message

    user_message = request.form['Body']

    # Getting information from session
    prev_conv = session.get(profile_name)
    if prev_conv:
        prev_message = prev_conv['message']
        prev_result = prev_conv['result']

        # Creating input for GPT

        history = [{"role": "user","content":prev_message}, {"role": "assistant","content":prev_result}, {"role": "user","content":user_message}]

    else:

        history = [{"role":"user","content":message}]


    # Getting input from GPT

    result = text_complition(history, user_info)

    # Debuging the result

    logger.debug(f"Result: {result['response']}")

    # Filling session

    session[profile_name] = {'message': user_message, "result": result['response']}

    if result['status'] == 1:
            send_message(sender_id, result['response'])
    else:
        return 'Error', 400
    return 'OK', 200
    
