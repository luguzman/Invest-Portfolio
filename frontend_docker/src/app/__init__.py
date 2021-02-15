from flask import Flask, jsonify, render_template, request, url_for, Response, send_from_directory
# from bson.json_util import dumps
# import dash
# from dash.dependencies import Input, Output
# import dash_core_components as dcc
# import dash_html_components as html
import json
import datetime
import requests
import logging
import pandas as pd
import time


# coins = ['ripple','bitcoin','ethereum','litecoin','iota','bitcoin_cash']
coins = ['ethereum']

logging.basicConfig(level=logging.INFO)

server = Flask(__name__, template_folder="templates", static_folder="static")

@server.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@server.route("/prueba", methods=["GET"])
def index2():
    return render_template("prueba.html")

@server.route("/home", methods=["GET"])
def home():
    return render_template("index.html")

@server.route("/crypto_portfolio", methods=["GET"])
def crypto_portfolio():
    return render_template("crypto_portfolio.html")

@server.route("/Asset_portfolio", methods=["GET"])
def asset_portfolio():
    nasdaq_info = open('/appdata/nasdaq_portfolio_info.json','r').read()
    logging.info("Nasdaq_info" +str(type(nasdaq_info)))
    logging.info(nasdaq_info)
    nasdaq_info = json.loads(nasdaq_info)
    stocks = pd.DataFrame(nasdaq_info['max_sharpe_allocation']).columns
    logging.info("Nasdaq_info" +str(len(nasdaq_info)))
    logging.info(nasdaq_info)
    with open("/appdata/nasdaq_portfolio_info_plot.html", "r") as p_graph:
        Nasdaq_portfolio = p_graph.read()

    asset_portfolio_text = render_template(
        "asset_portfolio.html", nasdaq_info = nasdaq_info, Nasdaq_portfolio = Nasdaq_portfolio, 
                            stocks = stocks
    )
    return asset_portfolio_text

@server.route("/crypto_forecast", methods=["GET"])
def crypto_forecast():
    for coin in coins:
        if coin == "ethereum":
            with open("/appdata/graph_{}.html".format(coin), "r") as eth:
                ethereum_graph = eth.read()
            with open("/appdata/history_graph_{}.html".format(coin), "r") as history_eth:
                ethereum_history_graph = history_eth.read()
        elif coin == "bitcoin":
            with open("/appdata/graph_{}.html".format(coin), "r") as f:
                bitcoin_graph = f.read()
        elif coin == "ripple":
            with open("/appdata/graph_{}.html".format(coin), "r") as g:
                ripple_graph = g.read()
        elif coin == "litecoin":
            with open("/appdata/graph_{}.html".format(coin), "r") as h:
                litecoin_graph = h.read()
        elif coin == "iota":
            with open("/appdata/graph_{}.html".format(coin), "r") as j:
                iota_graph = j.read()
    
    crypto_forecast_text = render_template(
            "crypto_forecast.html", coins = coins, ethereum_graph=ethereum_graph, 
                ethereum_history_graph = ethereum_history_graph
            # "crypto_forecast.html", coins = coins, ethereum_graph=ethereum_graph, bitcoin_graph = bitcoin_graph, 
            #             ripple_graph = ripple_graph, litecoin_graph = litecoin_graph, iota_graph = iota_graph
            )
    return crypto_forecast_text

@server.route("/get-csv/<csv_id>", methods=["GET"])
def get_csv(csv_id):
    logging.info("Obtaining csv ......")
    filename = f"{csv_id}.csv"

    logging.info(filename)
    try:
        with open("/appdata/{}".format(filename), "r") as e:
            csv_file = e.read()
    except FileNotFoundError:
        print("abort(404)")

    logging.info(csv_file)

    response = server.response_class(
        response=csv_file,
        mimetype='text/csv',
        headers={"Content-disposition":
                 "attachment; filename={}".format(filename)}
    )
    return response

@server.route('/handle_data', methods=['GET','POST'])
def handle_data():
    logging.info("Printing request")
    logging.info(request)
    logging.info(request.form['Asset1'])
    logging.info(request.form['Years'])

    # Gathering new assets from the frontend
    asset1 = request.form['Asset1']
    asset2 = request.form['Asset2']
    asset3 = request.form['Asset3']
    asset4 = request.form['Asset4']

    # Gathering the time window desired from the new assets
    years = request.form['Years']
    months = request.form['Months']
    days = request.form['Days']
    
    new_dict = {'asset1':asset1, 'asset2':asset2, 'asset3':asset3, 'asset4':asset4,
                    'years': years, 'months': months, 'days': days}
    logging.info(new_dict)

    requests.post("http://asset_portfolio:5001/nasdaq_function", json = json.dumps(new_dict))
    
    asset_info = open('/appdata/new_info.json','r').read()
    
    asset_info = json.loads(asset_info)
    stocks = pd.DataFrame(asset_info['max_sharpe_allocation']).columns

    with open("/appdata/new_info_plot.html", "r") as p_graph:
        asset_portfolio = p_graph.read()

    asset_portfolio_text = render_template(
        "asset_portfolio2.html", asset_info = asset_info, asset_portfolio = asset_portfolio, 
                            stocks = stocks
    )
    return asset_portfolio_text



if __name__ == '__main__':
    server.run(debug=True)


