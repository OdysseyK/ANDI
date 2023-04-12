import os


import openai
from dotenv import load_dotenv
from loguru import logger
load_dotenv()


openai.api_key = os.getenv('OPENAI_API_KEY')


def text_complition(msg, info):
    '''
    Call Openai API for text completion
    
    '''
    try:
        history = [{"role": "system","content": f'You are a chatbot and fitness motivator called Andi.You answer questions only about wellness and fitness and try to be concise. You will get information about customer via .json file. If you will get only customers name, ask customers about their info (height, weight, strength level from 1 to 10, workout days and time) first.\n{info}'}] + msg
        logger.debug(f"Hist + Message: {history}")
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=300,
        temperature=0.6,
        messages=history
        )

        logger.debug(f"Result: {response.choices[0].message.content}")

        return {
            'status': 1,
            'response': response.choices[0].message.content
        }
    except:
        return {
            'status': 0,
            'response': ''
        }

def entity_rec(msg):
    '''
    Call Openai API for entity recognition
    
    '''
    prompt = f"You are an entity recognition model. You need to extract customer's information and store it as .json file: Use only following keys to extract entities: height -'Height', weight -'Weight', activity level - 'Activity' and don't generate other text but json.\n\nText:{msg}\nOutput:"
    try:
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt = prompt,
        max_tokens=300,
        temperature=0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )
        return {
            'status': 1,
            'response': response.choices[0].text
        }
    except:
        return {
            'status': 0,
            'response': ''
        }
        
