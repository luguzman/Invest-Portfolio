import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.graphics.tsaplots as sgt
import statsmodels.tsa.stattools as sts
import plotly.graph_objects as go
import plotly.io as plio
import datetime
import warnings
import logging
import scipy.stats as stats
warnings.filterwarnings("ignore")

from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from scipy.stats.distributions import chi2 
from math import sqrt

logging.basicConfig(level=logging.INFO)

# create a N-order differenced series
def difference(dataset, interval=1):
    diff = list()
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i - interval]
        diff.append(value)
    return np.array(diff)

# invert differenced value
def inverse_difference(history, yhat, interval=1):
    history = list(history)
    n = len(yhat)
    if len(yhat) == 1:
        value = yhat[i] + history[-interval]
        history.append(value)
    else:
        value = yhat[0] + history[-interval]
        history.append(value)
        
        for i in range(1, n):
            value = yhat[i] + history[-interval]
            history.append(value)
    return np.array(history[-n:])

def ethereum_model(coin, data):

    # Dropping commas
    data['CLOSE']=data['CLOSE'].astype('str').str.replace(',','')
    data['OPENING']=data['OPENING'].astype('str').str.replace(',','')
    data['MAX_VALUE']=data['MAX_VALUE'].astype('str').str.replace(',','')
    data['MIN_VALUE']=data['MIN_VALUE'].astype('str').str.replace(',','')
    data['VOL']=data['VOL'].astype('str').str.replace(',','')

    # Convert fields except "DATE" in float fields
    cols = data.columns.drop('DATE_INFO')
    data[cols] = data[cols].apply(pd.to_numeric, errors='coerce')

    data.set_index("DATE_INFO", inplace=True)
    data = data.sort_index().asfreq('D')

    x = data.CLOSE.values

    # Regarding 1 ordered differenced time serie
    differenced = difference(x, 1)

    # Fitting model
    model_sar_5_i_0_ma_5 = SARIMAX(differenced, order=(5,0,5), seasonal_order = (1,0,1,7))
    results_sar_5_i_0_ma_5 = model_sar_5_i_0_ma_5.fit()

    forecast_sarima_5_0_5 = results_sar_5_i_0_ma_5.forecast(7) 

    predictions_sarima_5_0_5 = inverse_difference(data.CLOSE, forecast_sarima_5_0_5, interval = 1)
    final_df = create_final_df(predictions_sarima_5_0_5)

    # Saving plotly graph of historical data
    historical_data = create_df(data.reset_index())
    plio.write_html(plot_time_series(historical_data),'/appdata/history_graph_{}.html'.format(coin), include_plotlyjs=True)

    # Saving plotly graph of forecasted values.
    plio.write_html(plot_pred_time_series(final_df),'/appdata/graph_{}.html'.format(coin), include_plotlyjs=True)
    
    logging.info("Graph for {} saved".format(coin))
    print(datetime.datetime.now())

    return final_df

def create_df(data):
    df = pd.DataFrame({"DATE": data['DATE_INFO'],\
                        "CLOSE": data['CLOSE'],\
                        "MIN_VALUE": data['MIN_VALUE'],\
                        "MAX_VALUE": data['MAX_VALUE']}
                    )
    return df

def create_final_df(predictions):
    now = datetime.datetime.now()
    year = '{:02d}'.format(now.year)
    month = '{:02d}'.format(now.month)
    day = '{:02d}'.format(now.day)
    day2 = '{:02d}'.format(now.day + 6)
    hour = '{:02d}'.format(now.hour)
    minute = '{:02d}'.format(now.minute)
    day_month_year = '{}-{}-{}'.format(year, month, day)
    day_month_year2 = '{}-{}-{}'.format(year, month, day2)

    # We are considering the present day for prediction since webscrapper is downlaoding info until
    # the 1 day ago
    df = pd.DataFrame({"DATE":pd.date_range(day_month_year, day_month_year2),\
                        "FORECAST": np.round(predictions, 2),\
                        "MIN_VALUE": np.round(predictions - 19, 2),\
                        "MAX_VALUE": np.round(predictions + 19, 2)}
                    )
    return df

def plot_time_series(df):
    aux = df

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(aux['DATE']),
                    y=aux['CLOSE'],
                    name="Close price",
                    marker_color='rgb(100, 53, 39)',
                    mode="lines"
                    ))
    fig.update_layout(
        title='Historical ETH/USD close price',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Price in dollars $',
            titlefont_size=16,
            tickfont_size=14,
        )
    )
    fig.show()

    return fig

def plot_pred_time_series(final_df):
    aux = final_df

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(aux['DATE']),
                    y=aux['FORECAST'],
                    name="Forecast",
                    marker_color='rgb(100, 53, 39)',
                    mode="lines+text",
                    text=list(aux['FORECAST']),
                    textposition="top center"
                    ))
    fig.add_trace(go.Scatter(
                    name='Upper Bound',
                    x=list(aux['DATE']),
                    y=aux['MAX_VALUE'],
                    mode='lines',
                    marker=dict(color="#444"),
                    line=dict(width=0),
                    showlegend=False
                    ))
    fig.add_trace(go.Scatter(
                    name='Lower Bound',
                    x=list(aux['DATE']),
                    y=aux['MIN_VALUE'],
                    marker=dict(color="#444"),
                    line=dict(width=0),
                    mode='lines',
                    fillcolor='rgba(68, 68, 68, 0.3)',
                    fill='tonexty',
                    showlegend=False
                    ))
    fig.update_layout(
        title='One week ETH/USD forecast',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Price in dollars $',
            titlefont_size=16,
            tickfont_size=14,
        )
    )
    fig.show()

    return fig

    