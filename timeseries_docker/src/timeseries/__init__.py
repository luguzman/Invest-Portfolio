from flask import Flask,jsonify, render_template,request,Response
import json
import logging
import timeseries_functions
import requests
import pandas as pd
import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

def timeseriesmodel():
    resultjson={}
    # coins = ['ripple','bitcoin','ethereum','litecoin','iota','bitcoin-cash']
    coins = ['ethereum']
    for coin in coins:
        logging.info("Going to get info for " + coin)

        if coin == 'bitcoin-cash':
            coin = 'bitcoin_cash'

        req = requests.get('http://sqls:5003/querydf/{}'.format(coin))

        jonson = json.loads(req.text)

        coin_info = pd.read_json(jonson["result"])
        
        coin_info["DATE_INFO"] = coin_info["DATE_INFO"].apply(lambda x: datetime.datetime.fromtimestamp(x / 1e3))
        
        logging.info("Accessed the historical data of " + coin)

        coin_df = timeseries_functions.ethereum_model(coin,coin_info)

        resultjson = coin_df.to_json()

        print(coin_df.head())
        coin = 'pred_' + coin

        if coin == 'bitcoin-cash':
            coin = 'pred_bitcoin_cash'

        logging.info("Going to insert data from " + coin + " timeseries to SQL DB")
        requests.post('http://sqls:5003/insertpred/{}'.format(coin), json = json.dumps(resultjson))
        logging.info("Finish inserting data from prediction")


time.sleep(20)
# while True:
#     try:
#         timeseriesmodel()
#         scheduler = BackgroundScheduler()
#         job = scheduler.add_job(timeseriesmodel, 'interval', days=1)
#         scheduler.start()
#         break
#     except:
#         logging.info("Ya intente el time_series")
#         time.sleep(10)
timeseriesmodel()
