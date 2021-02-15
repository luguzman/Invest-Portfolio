import requests
import pandas as pd
import sqlalchemy
import datetime
import json
import logging
import yaml
import time
import base64
from sql_historical_functions import create_table
from sqlalchemy import create_engine,types
from flask import Flask, request

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

create_table()

@app.route("/querydf/<coin>", methods=['GET'])
def index(coin):
    logging.info(request.method + " requested")
    coin = str(coin)
    coin = coin.upper()
    logging.info("Query requested for " + coin)
    engine = sqlalchemy.create_engine('mysql://root:secret@db_sql:3306/crypto')
    logging.info("Connection initialized...")
    conn = engine.connect()
    logging.info("Connection established...")
    conn.execute("commit")
    logging.info("Query requested: select * from " + coin)
    rows = conn.execute("select * from " + coin)
    logging.info("Query executed...")
    conn.close()
    logging.info("Connection closed...")
    list_of_dicts = [{key: value for (key, value) in row.items()} for row in rows]
    dic = {}
    for k in list_of_dicts[0].keys():
        dic[k] = tuple(dic[k] for dic in list_of_dicts)
    result = pd.DataFrame(dic)
    return json.dumps({
            "result":result.to_json()
        })

@app.route("/querypred/<coin>", methods=['GET'])
def prediction(coin):
    logging.info(request.method + " requested")
    coin = str(coin)
    coin = "PRED_" + coin.upper()
    logging.info("Query requested for " + coin)
    engine = sqlalchemy.create_engine('mysql://root:secret@db_sql:3306/crypto')
    logging.info("Connection initialized...")
    conn = engine.connect()
    logging.info("Connection established...")
    conn.execute("commit")
    rows = conn.execute("select * from " + coin + " where DATE = '"+ datetime.datetime.today().strftime("%Y-%m-%d"+"'"))
    conn.close()

    list_of_dicts = [{key: value for (key, value) in row.items()} for row in rows]
    dic = {}
    for k in list_of_dicts[0].keys():
        dic[k] = tuple(dic[k] for dic in list_of_dicts)
    result = pd.DataFrame(dic)
    logging.info("Query result:")
    logging.info(result)
    return json.dumps({
            "result":result.to_json()
    })

@app.route("/insertdf/<coin>", methods=['POST'])
def insert(coin):
    logging.info(request.method + " requested")
    logging.info("Inserting information of " + coin + "to SQL DB")
    resultjson = request.get_json()
    values = pd.DataFrame(resultjson)
    values["DATE_INFO"] = values["DATE_INFO"].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    # values["CLOSE"] = values["CLOSE"].apply(lambda x: float(x.replace(',','')))
    # values["OPENING"] = values["OPENING"].apply(lambda x: float(x.replace(',','')))
    # values["MAX_VALUE"] = values["MAX_VALUE"].apply(lambda x: float(x.replace(',','')))
    # values["MIN_VALUE"] = values["MIN_VALUE"].apply(lambda x: float(x.replace(',','')))
    coin = str(coin)
    coin = coin.upper()
    engine = sqlalchemy.create_engine('mysql://root:secret@db_sql:3306/crypto')
    logging.info("Connection initialized...")
    conn = engine.connect()
    logging.info("Connection established...")
    conn.execute("commit")
    values.to_sql(coin,con=engine,index=False,if_exists='append')
    logging.info("Query executed...")
    conn.close()
    logging.info("Connection closed...")
    return "Data insertion is complete"


@app.route("/insertpred/<predcoin>", methods=['POST'])
def insertpred(predcoin):
    logging.info(request.method + " requested")
    resultjson = request.get_json()
    values = pd.DataFrame(yaml.load(json.loads(resultjson)))
    values["DATE"] = values["DATE"].apply(lambda x: pd.to_datetime(x, unit='ms'))
    values["FORECAST"] = values["FORECAST"].apply(lambda x: float(x))
    values["MIN_VALUE"] = values["MIN_VALUE"].apply(lambda x: float(x))
    values["MAX_VALUE"] = values["MAX_VALUE"].apply(lambda x: float(x))
    values.columns = ['DATE', 'FORECAST', 'MIN_VALUE', 'MAX_VALUE']
    predcoin = str(predcoin)
    predcoin = predcoin.upper()
    logging.info("Insertion requested for " + predcoin)
    engine = sqlalchemy.create_engine('mysql://root:secret@db_sql:3306/crypto')
    logging.info("Connection initialized...")
    conn = engine.connect()
    logging.info("Connection established...")
    conn.execute("commit")
    values.to_sql(predcoin, con=engine, index=False, if_exists='append')
    logging.info("Query executed...")
    conn.close()
    logging.info("Connection closed...")
    return "Data inserted succesfuly"

@app.route("/insertreal/<realcoin>", methods=['POST'])
def insertreal(realcoin):
    logging.info("I received a request " + request.method)
    logging.info("Someone is trying to write on the DB")
    resultjson = request.get_json()
    logging.info("The info to write is:")
    logging.info(resultjson)
    values = pd.DataFrame(resultjson)
    logging.info(values.head())
    logging.info("Beginning DF transformation...")
    values["time"] = values["time"].apply(lambda x: pd.to_datetime(x, unit='ms'))
    values["price"] = values["price"].apply(lambda x: float(x))
    values.columns = ["DATE", "PRICE"]
    logging.info("Result after transformation...")
    logging.info(values.head())
    realcoin = str(realcoin)
    realcoin = realcoin.upper()
    logging.info("The client is trying to write on " + realcoin)
    engine = sqlalchemy.create_engine('mysql://root:secret@db_sql:3306/crypto')
    logging.info("Connection initialized...")
    conn = engine.connect()
    logging.info("Connection established...")
    conn.execute("commit")
    values.to_sql("REAL_" + realcoin,con=engine,index=False,if_exists='append')
    logging.info("Data inserted")
    conn.close()
    logging.info("Connection closed")
    return "Insertion succesful"


@app.route("/queryreal/<coin>", methods=['GET'])
def readreal(coin):
    logging.info(request.method + " requested")
    coin = str(coin)
    coin = "REAL_" + coin.upper()
    logging.info("Query requested for " + coin)
    engine = sqlalchemy.create_engine('mysql://root:secret@db_sql:3306/crypto')
    logging.info("Connection initialized...")
    conn = engine.connect()
    logging.info("Connection established...")
    conn.execute("commit")
    rows = conn.execute("select * from " + coin + " order by DATE_R limit 1")
    logging.info("Query executed...")
    conn.close()
    logging.info("Connection closed...")
    list_of_dicts = [{key: value for (key, value) in row.items()} for row in rows]
    result = pd.DataFrame(list_of_dicts)
    logging.info("Query result:")
    logging.info(result)
    return json.dumps({
            "result":result.to_json()
    })

