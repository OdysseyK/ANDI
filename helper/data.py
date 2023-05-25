import pandas as pd
import numpy as np
import os
import json
from helper.openai_api import entity_rec_turbo, entity_rec
from loguru import logger
import requests




def get_user_data(user_id):
    df = pd.read_csv("gpt_data.csv").set_index("WaId")
    try:
        return df.loc[int(user_id)]
    except:
        return []

def save_user_data(text, name, w_id):
    df = pd.read_csv("gpt_data.csv").set_index("WaId")
    # measurements = entity_rec_turbo([{"role":"user","content":text}])['response']
    measurements = entity_rec(text)['response']
    try:

        json_m = json.loads(measurements)

    except:
        return False
    json_m['Name'] = name
    series = pd.Series(json_m)
    logger.debug(f"Series: {series}")
    series.name = int(w_id)
    df = df.append(series)
    df.to_csv("gpt_data.csv")
    return [True, json.loads(series.to_json())]
    
def get_verification(user_id):
    df = pd.read_csv("verification.csv").set_index("WaId")
    try:
        return df.loc[int(user_id)]
    except:
        return []

def set_verification(user_id, value):
    df = pd.read_csv("verification.csv").set_index("WaId")
    df.loc[int(user_id),"Status"] = value
    df.to_csv("verification.csv")
    
def get_sql(user_id, endpoint):
    req = requests.get(url=endpoint, params={'waid':user_id})
    return req.json()

def post_sql(data, endpoint):
    req = requests.post(url=endpoint, data=data)
    return req