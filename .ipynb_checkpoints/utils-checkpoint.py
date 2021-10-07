import pandas as pd
import numpy as np
from datetime import timedelta
import matplotlib.pyplot as plt

def ret_metrics(daily_ret_df):
    start_date, end_date = daily_ret_df.index[[0,-1]]
    years = (end_date - start_date).days/365
    
    #CGR
    CGR = (1 + daily_ret_df).cumprod() - 1
    CAGR = (CGR[-1] + 1)**(1/years) - 1
    
    #Information Ratios
    sharpe = daily_ret_df.mean()/daily_ret_df.std()
    rolling_sharpe = daily_ret_df.rolling(window=126).mean()/daily_ret_df.rolling(window=126).std()

    #Drawdown
    roll_max = (1+CGR).cummax()
    drawdown = (1+CGR)/roll_max - 1.0
    max_drawdown= drawdown.min()
    drawdown_times = (drawdown < 0).astype(np.int64)
    max_drawdown_duration = drawdown_times.groupby((drawdown_times != drawdown_times.shift()).cumsum()).cumsum().min()
    
    #Win/Loss percentage
    winners = (daily_ret_df > 0).sum() / ((daily_ret_df > 0).sum() + (daily_ret_df < 0).sum())
    losers = (daily_ret_df < 0).sum() / ((daily_ret_df > 0).sum() + (daily_ret_df < 0).sum())
    
    print(f'CAGR: {np.round(100*CAGR,2)}% \nAnnual Sharpe Ratio: {round(252**0.5 * sharpe,2)} \
          \nWin Percetage: {np.round(100*winners, 2)}% \
          \nLoss Percetage: {np.round(100*losers, 2)}% \
          \nMax win: {np.round(100*daily_ret_df.max(),2)}% \
          \nMax Loss: {np.round(100*daily_ret_df.min(),2)}% \
          \nAverage Win/Loss: {np.round(100*daily_ret_df.mean(), 2)}% \
          \nMax Drawdown: {np.round(100*max_drawdown,2)}% \
          \nMax Drawdown Duration: {max_drawdown_duration} \
          \n\n')
    
    CGR.plot()
    plt.title('Cummulative Growth')
    plt.show()
    
    drawdown.plot()
    plt.title('Drawdown')
    plt.show()
    return drawdown

def all_strats(daily_rets, weights):
    if np.sum(weights) != 1:
        raise ValueError('Weights do not add to 1')
    total_daily_rets = 0
    for i in range(len(daily_rets)):
        total_daily_rets = total_daily_rets + daily_rets[i]*weights[i]
    return total_daily_rets