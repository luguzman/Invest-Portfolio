'''
###########################################################################################
##     Here is the service of the Webscraper Historical prices of the cryptocurrencies   ##
##     Communication with SQL DB                                                         ##
###########################################################################################
'''

# -------------------------------- Import Packages ----------------------------------------
import json
import logging
import webscraper_hist_functions
import datetime
import requests
import time
from flask import Flask,jsonify, render_template,request,Response
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# -------------------------------- Functions ---------------------------------------------

# This funtion gives you the historical information prices (without communication with SQL)
def writedf(coin):
    logging.info("Starting webscraping...")
    histdf = webscraper_hist_functions.retrieve(coin, '20170310', datetime.datetime.today().strftime('%Y-%m-%d').replace('-',''))
    logging.info("Webscraping succesful...")
    logging.info(histdf.head())
    histdf.columns = ['DATE_INFO', 'OPENING', 'CLOSE', 'MIN_VALUE', 'MAX_VALUE', 'VOL', 'MARKET_CAP']
    histdf["DATE_INFO"] = histdf["DATE_INFO"].apply(lambda x: datetime.datetime.strftime(x, '%Y-%m-%d'))
    resultjson = histdf[[ 'DATE_INFO', 'CLOSE', 'OPENING', 'MAX_VALUE', 'MIN_VALUE', 'VOL']].to_dict()
    if coin == 'bitcoin-cash':
        coin = 'bitcoin_cash'
        
    logging.info("Inserting historical info to SQL DB")
    req = requests.post('http://sqls:5003/insertdf/{}'.format(coin), json = resultjson)

    logging.info("I inserted historical data of " + coin + " in sql service")

success =  False
while not success:
    try:
        time.sleep(12)
        # coins = ['ripple','bitcoin','ethereum','litecoin','iota','bitcoin-cash']
        coins = ['ethereum']
        for coin in coins:
            logging.info("Webscraping process for " + coin)
            writedf(coin)
        success = True
    except:
        success = False


