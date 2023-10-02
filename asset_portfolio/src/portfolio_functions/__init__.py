import pandas as pd  
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sco
import yfinance
import plotly.graph_objects as go
from datetime import datetime
import plotly.io as plio



def plot_evolution_stock(raw_data):
    plt.figure(figsize=(14, 7))

    for c in raw_data.columns.values:
        plt.plot(raw_data.index, raw_data[c], lw=3, alpha=0.8,label=c)
    plt.legend(loc='upper left', fontsize=12)
    plt.ylabel('price in $')
    plt.show()

def daily_returns(raw_data):
    returns = raw_data.pct_change()

    plt.figure(figsize=(14, 7))
    for c in returns.columns.values:
        plt.plot(returns.index, returns[c], lw=3, alpha=0.8,label=c)
    plt.legend(loc='upper right', fontsize=12)
    plt.ylabel('daily returns')
    plt.show()

def portfolio_annualised_performance(weights, mean_returns, cov_matrix):
    returns = np.sum(mean_returns*weights ) *252 #252: number of trading days in one year
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252) #weights is 1x4 & cov_matrix is 
    return std, returns

def random_portfolios(num_portfolios, mean_returns, cov_matrix, risk_free_rate):
    results = np.zeros((3,num_portfolios)) # Matrix of 3xN since we are going to save std, returns and sharpe ratio
    weights_record = []
    for i in range(num_portfolios):
        weights = np.random.random(4)
        weights /= np.sum(weights)
        weights_record.append(weights)
        portfolio_std_dev, portfolio_return = portfolio_annualised_performance(weights, mean_returns, cov_matrix)
        results[0,i] = portfolio_std_dev
        results[1,i] = portfolio_return
        results[2,i] = (portfolio_return - risk_free_rate) / portfolio_std_dev
    return results, weights_record


# Remeber that portfolio_annualised_performance returns sd and returns of each generated portfolio
def neg_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate):
    p_var, p_ret = portfolio_annualised_performance(weights, mean_returns, cov_matrix)
    return -(p_ret - risk_free_rate) / p_var

def max_sharpe_ratio(mean_returns, cov_matrix, risk_free_rate):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix, risk_free_rate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = (0.0,1.0)
    bounds = tuple(bound for asset in range(num_assets))
    result = sco.minimize(neg_sharpe_ratio, num_assets*[1./num_assets,], args=args,
                        method='SLSQP', bounds=bounds, constraints=constraints)
    return result

def portfolio_volatility(weights, mean_returns, cov_matrix):
    return portfolio_annualised_performance(weights, mean_returns, cov_matrix)[0]

def min_variance(mean_returns, cov_matrix):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = (0.0,1.0)
    bounds = tuple(bound for asset in range(num_assets))

    result = sco.minimize(portfolio_volatility, num_assets*[1./num_assets,], args=args,
                        method='SLSQP', bounds=bounds, constraints=constraints)

    return result

def efficient_return(mean_returns, cov_matrix, target):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix)

    def portfolio_return(weights):
        return portfolio_annualised_performance(weights, mean_returns, cov_matrix)[1]

    constraints = ({'type': 'eq', 'fun': lambda x: portfolio_return(x) - target},
                   {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0,1) for asset in range(num_assets))
    result = sco.minimize(portfolio_volatility, num_assets*[1./num_assets,], args=args, method='SLSQP', bounds=bounds, constraints=constraints)
    return result


def efficient_frontier(mean_returns, cov_matrix, returns_range):
    efficients = []
    for ret in returns_range:
        efficients.append(efficient_return(mean_returns, cov_matrix, ret))
    return efficients

def display_calculated_ef_with_random(mean_returns, cov_matrix, num_portfolios, risk_free_rate, raw_data, name="Nasdaq_potfolio"):
    # Generating random portfolios and saving each volatility, return & sharpe ratio in results variable
    results, weights = random_portfolios(num_portfolios,mean_returns, cov_matrix, risk_free_rate) 
    # Notice that to find the portfolio with the best sharpe ratio we won't use weights netheir results this was only
    # for generating random portfolios and to compare it with the result that we'll obtain in the next part:
    
    max_sharpe = max_sharpe_ratio(mean_returns, cov_matrix, risk_free_rate) # results of optimizing sharpe ratio equation
    sdp, rp = portfolio_annualised_performance(max_sharpe['x'], mean_returns, cov_matrix) # x: Are the weights 
    max_sharpe_allocation = pd.DataFrame(max_sharpe.x,index=raw_data.columns,columns=['allocation'])
    max_sharpe_allocation.allocation = [round(i*100,2)for i in max_sharpe_allocation.allocation]
    max_sharpe_allocation = max_sharpe_allocation.T
    
    min_vol = min_variance(mean_returns, cov_matrix) # results of minimizing volatility
    sdp_min, rp_min = portfolio_annualised_performance(min_vol['x'], mean_returns, cov_matrix)
    min_vol_allocation = pd.DataFrame(min_vol.x,index=raw_data.columns,columns=['allocation'])
    min_vol_allocation.allocation = [round(i*100,2)for i in min_vol_allocation.allocation]
    min_vol_allocation = min_vol_allocation.T
    
    print ("-"*80)
    print ("Maximum Sharpe Ratio Portfolio Allocation\n")
    print ("Annualised Return:", round(rp,2))
    print ("Annualised Volatility:", round(sdp,2))
    print ("\n")
    print (max_sharpe_allocation)
    print ("-"*80)
    print ("Minimum Volatility Portfolio Allocation\n")
    print ("Annualised Return:", round(rp_min,2))
    print ("Annualised Volatility:", round(sdp_min,2))
    print ("\n")
    print (min_vol_allocation)
    
    aux = pd.DataFrame(results)
    target = np.linspace(rp_min, rp - 0.01, 100)
    efficient_portfolios = efficient_frontier(mean_returns, cov_matrix, target)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=aux.iloc[0,:],
                    y=aux.iloc[1,:],
                    name="Portfolio",
                    #marker_color=aux.iloc[0,:], 
                    mode="markers",
                    marker=dict(color= aux.iloc[0,:], 
                          colorscale='Viridis', size=4, colorbar=dict(thickness=10))
                    ))
    fig.add_trace(go.Scatter(x=[sdp],
                    y=[rp],
                    name="Optimal Portfolio",
                    mode="markers",
                    marker=dict(size=[20],
                                color=["darkred"]),
                    marker_symbol = "star"                        
                    ))
    fig.add_trace(go.Scatter(x=[sdp_min],
                    y=[rp_min],
                    name="Minimum Risk Portfolio",
                    mode="markers",
                    marker=dict(size=[20],
                                color=["lightcoral"]),
                    marker_symbol = "star"                        
                    ))
    fig.add_trace(go.Scatter(x=[p['fun'] for p in efficient_portfolios],
                    y=target,
                    name="Efficient frontier",
                    #marker_color=aux.iloc[0,:], 
                    mode="markers",
                    marker=dict(color= "indianred", 
                              size=4),
                    marker_symbol = "square"                
                    ))
    fig.update_layout(
        title="Portfolio with:" + str(raw_data.columns.values),
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Returns',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=1.1,
            y=1.0
        )
    )
    fig.update_xaxes(title_text = "Volatility")

    plio.write_html(fig, '/appdata/{}.html'.format(name), include_plotlyjs = True)
    return rp, sdp, max_sharpe_allocation, rp_min, sdp_min, min_vol_allocation, target, efficient_portfolios