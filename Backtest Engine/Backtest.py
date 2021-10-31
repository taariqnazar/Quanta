import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

from Portfolio2 import Portfolio
from Strategy import Strategy, TS_Forecast

class Backtest:
    def __init__(self, start, end, symbols, model_symbols, capital=1e4, stop_loss=0.65):
        self.start = start
        self.end = end
        
        model_data = yf.Ticker(model_symbols, start='2012-05-01', end=start)
        params_list =  pd.DataFrame([[0, 1, 0],
            [0, 1, 1],
            [1, 1, 0],
            [2, 1, 3],
            [4, 1, 2],
            [3, 1, 4]], columns=[['p', 'i', 'q']])

        strategy = TS_Forecast(params_list, model_data)
        self.portfolio = Portfolio(symbols, capital, strategy, stop_loss=stop_loss)

    def run(self, market_data):
        for date, price_bar in market_data.iterrows():
            price_bar = pd.DataFrame(price_bar).T
            self.portfolio.step(price_bar)