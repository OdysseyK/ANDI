from helper.openai_api import text_complition
from helper.twilio_api import send_message
from helper.data import get_user_data, save_user_data, get_sql, post_sql
from src.prompts import get_prompt

from flask import Flask, request, session
from dotenv import load_dotenv
from loguru import logger
import os

import requests
import pandas as pd
import json
import numpy as np


load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(12).hex()  # os.getenv("SECRET_KEY")

@app.route('/')
def home():
    return 'All is well...'


@app.route('/twilio/receiveMessage', methods=['POST'])
def receiveMessage():

    logger.debug(f"Session Before: {session}")

    get_endpoint = "https://api-dev.worqout.io/api/v5/users/andi/get-log"
    send_endpoint = "https://api-dev.worqout.io/api/v5/users/andi/register-log"
    
    welcome_text = "¡Hola! Soy ANDI, tu asistente y motivador de fitness. Antes de empezar, tengo algunas preguntas que podrían ayudarme a entenderte mejor."
    
    # Getting information from Whatsapp

    profile_name = request.form['ProfileName']
    sender_id = request.form['From']
    wa_id = request.form['WaId']

    user_message = request.form['Body']

    # # Checking verification
    # ver_phrase = get_verification(wa_id)['Passphrase']
    # ver_status = get_verification(wa_id)['Status']
    # is_verificated = user_message == ver_phrase
    
    # logger.debug(f"VER PHRASE: {ver_phrase}")
    # logger.debug(f"VER STATUS: {ver_status}")
    # if not ver_status and is_verificated:
        # send_message(sender_id, "Done!")
        # set_verification(wa_id, 1)
        # return 'OK', 200
    # elif not ver_status and not is_verificated:
        # return 'OK', 200

        

    # Checking if the user has data in the database

    user_data = get_user_data(wa_id)
    sql_user_data = get_sql(int(wa_id), get_endpoint)
    logger.debug(f"SQL User Data: {sql_user_data}\nLen: {len(sql_user_data)}")

    # Debuging the information

    logger.debug(f"User: {profile_name}")
    logger.debug(f"From: {sender_id}")

    # Getting user message

   

    # Getting information from session
    prev_conv = session.get(profile_name, {})
    
    if prev_conv and prev_conv.get("result"):
    
        prev_message = prev_conv['message']
        prev_result = prev_conv['result']

        # Creating input for GPT

        history = [{"role": "user","content":prev_message}, {"role": "assistant","content":prev_result}, {"role": "user","content":user_message}]

    else:
        history = [{"role":"user","content":user_message}]

    # Checking the availability of the user's information

    if len(user_data) == 11 and not session.get(profile_name, {}).get("keys", {}):

        # Getting input from GPT
        user_data_json = "\n".join(user_data.to_json()[1:-1].split(","))

        logger.debug(f"JSON: {user_data_json}")
        result = text_complition(history, user_data_json)
        
    # elif prev_conv:
# 
        # flag = save_user_data(user_message, profile_name, wa_id)
        # if flag:
            # send_message(sender_id, "Thank you for your time!")
            # session[profile_name] = {'message': user_message, "result": "Thank you for your time!"}
            # return 'OK', 200
        # else:
            # send_message(sender_id, "Please can you provide full information?")
            # session[profile_name] = {'message': user_message, "result": "Please can you provide full information?"}
            # return 'OK', 200

    else:
        # Setting keys to obtain prompts
        
        keys = ['Height', 'Weight', 'Gender', 'Activity Level', 'Fitness Level', 'Goal', 'Training Environment', 'SmartWatch', 'AI Scan Permission']

        # Getting remaining keys
        rem_keys = session.get(profile_name, {}).get("keys")
        user_inputs = session.get(profile_name, {}).get('inputs', [])
        logger.debug(f"INPUTS: {user_inputs}")
        
        
        if rem_keys:
        
            # Getting the first key to ask question
            
            key = rem_keys.pop(0)
            send_message(sender_id, get_prompt(key))

            # Updating keys
            
            session[profile_name]['keys'] = rem_keys
            
        elif not rem_keys and 1<=len(user_inputs)<10:

            
            keys = user_data.columns[user_data.isna().any()].tolist() # getting unfilled data columns
            key = keys.pop(0)
            session[profile_name]['keys'] = keys
            send_message(sender_id, "Perdón, algo salió mal. Me puedes responder de nuevo:" + '\n' + get_prompt(key))

        elif not rem_keys and len(user_inputs)==10:
        
            user_text = ','.join(session[profile_name]['inputs'])
            
            flag = save_user_data(user_text, profile_name, wa_id)
            if flag[0]:
                send_message(sender_id, "¡Gracias por tu tiempo!")
                flag[1]["wa_id"] = wa_id
                flag[1] = {i.lower(): j for i, j in flag[1].items()}
                req = post_sql(flag[1], send_endpoint)
                logger.debug(f"POST SQL: {req}")
                session[profile_name] = {'message': user_message, "result": "¡Gracias por tu tiempo!"}
                return 'OK', 200
            else:
                return 'Error', 400
        else:
            # Setting keys and name for new users
            session[profile_name] = {}
            session[profile_name]['keys'] = keys
            send_message(sender_id, welcome_text + '\n' + get_prompt('Birthdate'))

        temp = session[profile_name].get('inputs',[])
        temp.append(user_message)
        session[profile_name]['inputs'] = temp
        session.modified = True
        logger.debug(f"Session: {session}")
        logger.debug(f"Session inputs: {session.get('inputs')}")
        return 'OK', 200
    
        

    
    # Filling session

    session[profile_name] = {'message': user_message, "result": result['response']}
    logger.debug(f"Session After: {session}")

    if result['status'] == 1:
            send_message(sender_id, result['response'])
    else:
        return 'Error', 400
    return 'OK', 200
    
