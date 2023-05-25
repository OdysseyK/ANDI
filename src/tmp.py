from helper.openai_api import text_complition
from helper.twilio_api import send_message
from helper.data import get_user_data, save_user_data
from prompts import get_prompt

from flask import Flask, request, session
from dotenv import load_dotenv
from loguru import logger
import os


import pandas as pd
import json
import numpy as np


load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(12).hex() # FIX IT

@app.route('/')
def home():
    return 'All is well...'


@app.route('/twilio/receiveMessage', methods=['POST'])
def receiveMessage():

    logger.debug(f"Session Before: {session}")


    welcome_text = "Hello there! I'm ANDI, your fitness assistant and motivator. I would like to ask you a few questions about your physical activity and body measurements."

    # Getting information from Whatsapp

    profile_name = request.form['ProfileName']
    sender_id = request.form['From']
    wa_id = request.form['WaId']

    # Checking if the user has data in the database

    user_data = get_user_data(wa_id)
    

    logger.debug(f"User Data: {user_data}")

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
        session[profile_name] = {}
        history = [{"role":"user","content":user_message}]

    # Checking the availability of the user's information

    if user_data.shape[0] == 10 and not session.get("keys"):

        # Getting input from GPT

        result = text_complition(history, profile_name)
        
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
        
        keys = ['Height', 'Weight', 'Gender', 'Activity', 'Fitness', 'Goal', 'Place', 'Watch', 'Scan']

        # Getting remaining keys
        rem_keys = session.get(profile_name).get("keys")
        
        if rem_keys:
        
            # Getting the first key to ask question
            
            key = rem_keys.pop(0)
            send_message(sender_id, get_prompt(key))

            # Updating keys
            
            session[profile_name]['keys'] = rem_keys
            
        elif not rem_keys and user_data.shape[0] < 10:

            
            keys = user_data.columns[user_data.isna().any()].tolist() # getting unfilled data columns
            key = keys.pop(0)
            session[profile_name]['keys'] = keys
            send_message(sender_id, "Sorry, something went wrong. Can you please answer again:" + '\n' + get_prompt(key))

        elif not rem_keys and user_data.shape[0] == 10:
        
            session[profile_name] = session[profile_name].pop("key")
            user_text = session[profile_name]['message']
            
            flag = save_user_data(user_text, profile_name, wa_id)
            if flag:
                send_message(sender_id, "Thank you for your time!")
                session[profile_name] = {'message': user_message, "result": "Thank you for your time!"}
                return 'OK', 200
            else:
                return 'Error', 400
                
            
        else:
            # Setting keys and name for new users
            
            session[profile_name]['keys'] = keys
            session[profile_name]['name'] = profile_name
            session[profile_name]['message'] = ''
            send_message(sender_id, welcome_text + '\n' + get_prompt('Birthdate'))

            
        
        session[profile_name]['message'] = session[profile_name]['message'] + ',' + user_message
        logger.debug(f"Session: {session}")
        return 'OK', 200
    
        

        
    
    # Filling session

    session[profile_name] = {'message': user_message, "result": result['response']}
    logger.debug(f"Session After: {session}")

    if result['status'] == 1:
            send_message(sender_id, result['response'])
    else:
        return 'Error', 400
    return 'OK', 200
    
