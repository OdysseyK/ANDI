from helper.openai_api import text_complition
from helper.twilio_api import send_message
from helper.data import get_user_data, save_user_data


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


    welcome_text = "Hello there! I'm ANDI, your fitness assistant and motivator. I would like to ask you a few questions about your physical activity and body measurements.\n1. What is your height in centimeters?\n2. What is your current weight in kilograms?\n3. How would you describe your level of physical activity? Would you say you are not active at all, moderately active, active, or very active?\nThank you for your responses! Based on this information, I can give you personalized advices and fitness plan that suits your needs and goals!"

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

        history = [{"role":"user","content":user_message}]

    # Checking the availability of the user's information

    if user_data:

        # Getting input from GPT

        result = text_complition(history, profile_name)
        
    elif prev_conv:

        flag = save_user_data(user_message, profile_name, wa_id)
        if flag:
            send_message(sender_id, "Thank you for your time!")
            session[profile_name] = {'message': user_message, "result": "Thank you for your time!"}
            return 'OK', 200
        else:
            send_message(sender_id, "Please can you provide full information?")
            session[profile_name] = {'message': user_message, "result": "Please can you provide full information?"}
            return 'OK', 200

    else:

        send_message(sender_id, welcome_text)
        session[profile_name] = {'message': user_message, "result": "Welcome!"}
        return 'OK', 200
    
        

        
    
    # Filling session

    session[profile_name] = {'message': user_message, "result": result['response']}
    logger.debug(f"Session After: {session}")

    if result['status'] == 1:
            send_message(sender_id, result['response'])
    else:
        return 'Error', 400
    return 'OK', 200
    
