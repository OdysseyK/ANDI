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
        history = [{"role": "system","content": f"You are a chatbot and fitness motivator called ANDI (Adaptive Nurturing Digital Intelligence) created by Worqout. You must speak only in Spanish and answer questions only about wellness and fitness and try to be concise. You will get information about the customer. Use them to answer questions related to macros, nutrition, etc. Don't ask for more information.\nInfo:\n{info}"}] + msg
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

def entity_rec_eng(msg):
    '''
    Call Openai API for entity recognition
    
    '''
    prompt = f"Extract customer's information and store it as .json file: Use only following keys to extract information: height -'Height', weight -'Weight', activity level - 'Activity', birthdate - 'Birthdate', availability of smart watch 'Watch', fitness level - 'Fitness', training environment - 'Environment', fitness goal - 'Goal', gender - 'Gender', permission to do AI body scan - 'Scan' .If you have missing even one information ask for it.  Don't generate other text but json.\n\nText:{msg}\nOutput:"
    try:
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt = prompt,
        max_tokens=250,
        temperature=0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )
        logger.debug(f"Result: {response.choices[0].text}")

        return {
            'status': 1,
            'response': response.choices[0].text
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
    prompt = f"Extraer la información del cliente y almacenarla como archivo .json: Utilice solo las siguientes claves para extraer la información: altura - 'Height', peso - 'Weight', nivel de actividad - 'Activity', fecha de nacimiento - 'Birthdate', disponibilidad de reloj inteligente - 'Watch', nivel de condición física - 'Fitness', entorno de entrenamiento - 'Environment', objetivo de condición física - 'Goal', género - 'Gender', permiso para realizar escaneo corporal de IA - 'Scan'. Si falta aunque sea una información, solicítela. No genere otro texto que no sea json\n\nTexto:{msg}\nOutput:"
    try:
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt = prompt,
        max_tokens=250,
        temperature=0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )
        logger.debug(f"Result: {response.choices[0].text}")

        return {
            'status': 1,
            'response': response.choices[0].text
        }
    except:
        return {
            'status': 0,
            'response': ''
        }


def entity_rec_turbo(msg):
    '''
    Call Openai API for entity recognition using chatGPT
    
    '''
    try:
        history = [{"role": "system","content": "Extract customer's information and store it as .json file: Use only following keys to extract entities: height -'Height', weight -'Weight', activity level - 'Activity'. If you have missing even one entity . Don't generate other text but json."}] + msg
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=200,
        temperature=0,
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
