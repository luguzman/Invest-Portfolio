import scipy.optimize as sco
import yfinance
import json
import logging
from datetime import datetime
from portfolio_functions import *
from dateutil.relativedelta import relativedelta

from flask import Flask,jsonify,render_template,request,Response

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


@app.route("/nasdaq_function", methods=['POST'])
def elements():
    logging.info("Generating new portfolio info")
    r = request.get_json()
    logging.info(r)
    logging.info(type(r))

    new_info_dict = json.loads(r)
    logging.info(new_info_dict)
    logging.info(type(new_info_dict))
    asset1 = new_info_dict['asset1']
    asset2 = new_info_dict['asset2']
    asset3 = new_info_dict['asset3']
    asset4 = new_info_dict['asset4']
    years = new_info_dict['years']
    months = new_info_dict['months']
    days = new_info_dict['days']

    nasdaq_portfolio(asset1, asset2, asset3, asset4, "new_info", years, months, days)
    
    return logging.info("New portfolio generated")


def nasdaq_portfolio(asset1='AAPL', asset2='AMZN', asset3='GOOGL', asset4='FB', 
                        name="nasdaq_portfolio_info", years=2, months=0, days=0):
    

    now = datetime.now()
    str_year = str(now.year)
    str_month = str(now.month)
    str_day = str(now.day)
    str_today = str_year + '-' + str_month + '-' + str_day

    logging.info("Running nasdaq_portfolio function")
    logging.info(type(years))
    str_init_date = datetime.strftime(datetime.strptime(str_today, "%Y-%m-%d") - relativedelta(years=int(years)) 
                                                                               - relativedelta(months=int(months))
                                                                               - relativedelta(days=int(days)), "%Y-%m-%d")


    stocks = [str(asset1),str(asset2),str(asset3),str(asset4)]
    raw_data = yfinance.download (tickers = stocks, start = str_init_date,
                end = str_today, interval = "1d", group_by = 'ticker', auto_adjust = True, treads = True)

    logging.info(stocks)
    logging.info(raw_data)
    raw_data = raw_data[[( stocks[0],  'Close'),( stocks[1],  'Close'),( stocks[2],  'Close'),( stocks[3],  'Close')]]
    raw_data.columns=[stocks[0],stocks[1],stocks[2],stocks[3]]
    
    # Plotting evolution of the assets
    # plot_evolution_stock(raw_data)

    # Plotting daily returns 
    # daily_returns(raw_data)

    returns = raw_data.pct_change()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    num_portfolios = 5000
    risk_free_rate = 0.0012 #.0013 actualmente 14 OCT 2020

    logging.info("Creating asset portfolio info & plot")
    # Create and save portafolio information & plot
    rp, sdp, max_sharpe_allocation, rp_min, sdp_min, min_vol_allocation, target, efficient_portfolios = display_calculated_ef_with_random(mean_returns, 
                                                                                                        cov_matrix, num_portfolios, risk_free_rate, raw_data,
                                                                                                        name=name+"_plot")
    logging.info("Assets portfolio plot info saved")

    assets_dict = str({"rp": round(rp,4), "sdp": round(sdp,4), "max_sharpe_allocation":max_sharpe_allocation.to_dict(),
             "rp_min": round(rp_min,4), "sdp_min": round(sdp_min,4), "min_vol_allocation":min_vol_allocation.to_dict()})
    assets_dict = assets_dict.replace("'","\"")

    weights_efficient_frontier = {stocks[0]:[], stocks[1]:[], stocks[2]:[], stocks[3]:[]}
    for i in range(len(efficient_portfolios)):
        for w in range(0,4):
            weights_efficient_frontier[stocks[w]].append(efficient_portfolios[i]['x'][w])

    efficient_frontier_portfolios = pd.DataFrame({'returns':target, 
              stocks[0]: np.round(weights_efficient_frontier[stocks[0]],4), 
              stocks[1]: np.round(weights_efficient_frontier[stocks[1]],4),
              stocks[2]: np.round(weights_efficient_frontier[stocks[2]],4), 
              stocks[3]: np.round(weights_efficient_frontier[stocks[3]],4)})

    logging.info("Saving returns and weights from portfolios of the efficient frontier of delivered assets")
    efficient_frontier_portfolios.to_csv("/appdata/efficient_frontier_portfolios.csv")

    logging.info(type(assets_dict))
    with open('/appdata/{}.json'.format(name), 'w') as f:
        f.write(assets_dict)   
        
    logging.info("Assets portfolio info saved")



nasdaq_portfolio()