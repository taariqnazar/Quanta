import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import timedelta

from models import TS_Ensemble

import warnings
warnings.filterwarnings("ignore")

class Portfolio():
    def __init__(self, symbols, start, end, amount, ftc=0.0, ptc=0.0, verbose = True):
        self.symbols = symbols
        self.start = start
        self.end = end 
        self.initial_amount = amount
        self.amount = amount
        self.ftc = ftc
        self.ptc = ptc
        #self.positions = pd.DataFrame([np.zeros(len(symbols))], columns = symbols)
        self.trades = 0
        self.days_traded = 0
        self.verbose = verbose
        self.initialize_data()
        self.positions = pd.DataFrame([np.zeros(len(self.market_data.columns))], columns = self.market_data.columns)

        #OMX
        best_params = pd.DataFrame([[0, 1, 0],
            [0, 1, 1],
            [1, 1, 0],
            [2, 1, 3],
            [4, 1, 2],
            [3, 1, 4]], columns=[['p', 'i', 'q']])
        #DAX
        """
        best_params = pd.DataFrame([[3, 1, 2],
            [3, 1, 3],
            [0, 1, 0],
            [1, 1, 0]], columns=[['p', 'i', 'q']])
        """
        self.model = TS_Ensemble(best_params, self.model_data.loc[:'2021-01-29'])

    def initialize_data(self, OHLC='Close'):
        tickers = ' '.join([str(elem) for elem in self.symbols])
        data = yf.Ticker(tickers).history(start=self.start, end=self.end)[OHLC].ffill()
        self.model_data = data
        #OMX
        self.market_data = pd.read_csv('./data/omx_minif_LS_2021-02-01_2021-10_29.csv', decimal= ',', index_col=0)
        #DAX
        #self.market_data = pd.read_csv('./data/dax_minif_LS_2021-02-01_2021-10_29.csv', decimal= ',', index_col=0)
        
    def get_date(self,price_bar):
        date = str(price_bar.index.values[0])[:10]
        return date
    
    def print_balance(self, price_bar):
        date = self.get_date(price_bar)
        print(f'{date} | current balance {self.amount:.2f}')
    
    def get_net_value(self, price_bar):
        return (price_bar.reset_index(drop=True)*abs(self.positions)).sum(axis=1)[0] + self.amount
    
    def print_net_value(self, price_bar):
        date = self.get_date(price_bar)
        #Check this 
        net_wealth = self.get_net_value(price_bar)
        print(f'{date} | current net wealthh {net_wealth:.2f}')
    """
    def place_order(self, symbol, price_bar, direction, amount=None):
        date = self.get_date(price_bar)
        price = price_bar[symbol][0]
        
        if amount is None:
            amount = self.amount
        
        units = direction*int(amount/price)
        
        #If short then sell of all my longs and take full positions in short

        if units != 0:
            self.amount -= (units*price)*(1 + direction*self.ptc) + self.ftc
            self.positions[symbol] += units
            self.trades += 1

            if self.verbose:
                order_type = 'BUY' if direction == 1 else 'SELL'
                print(f'{date} | {order_type} {abs(units)} units of {symbol} at {price:.2f}')
                self.print_balance(price_bar)
                self.print_net_value(price_bar)

    def place_orders(self, symbols, price_bar, weights, amount = None):
        if not amount:
            amount = self.amount
            
        for symbol in symbols:
            weight = weights[symbol][0]
            direction = np.sign(weight)
            allocation = np.abs(weight)*amount
                
            self.place_order(symbol, price_bar, direction, allocation)
    """
    def place_order(self, symbol, price_bar, units):
        date = self.get_date(price_bar)
        if units != 0:
            price = price_bar[symbol][0]

            self.amount -= units*price*(1 + self.ptc) + self.ftc
            self.positions[symbol] += units
            self.trades += 1

            if self.verbose:
                print(f'{date} | Order {units} units of {symbol} at {price:.2f}')
                self.print_balance(price_bar)
                self.print_net_value(price_bar)
            
    def rebalance_positions(self, price_bar, weights):
        """
        Goal: Get from old positions to new positions.
        """
        #If short then exit all positions that are long

        if weights['Long'][0] == 1:
            #Unwind prev shorts
            units = -self.positions['Short'][0]
            self.place_order('Short', price_bar, units)
            
            #Load new longs
            units = int(self.amount/price_bar['Long'][0])
            self.place_order('Long', price_bar, units)

        if weights['Short'][0] == 1:
            #Unwind prev longs
            units = -self.positions['Long'][0]
            self.place_order('Long', price_bar, units)

            #Load new longs
            units = int(self.amount/price_bar['Short'][0])
            #self.place_order('Short', price_bar, units)

    def get_current_weights(self, symbols, price_bar):
        net_value = self.get_net_value(price_bar)
        weights = (price_bar.reset_index(drop=True)*self.positions)/net_value
        return weights
    
    def close_out(self, price_bar):
        date = self.get_date(price_bar)
        self.amount += (price_bar.reset_index(drop=True)*self.positions).sum(axis=1)[0]
        self.positions = 0*self.positions
        self.trades += np.abs(self.positions>0).sum(axis=1)[0]
        #if self.verbose:
        print(f'{date} | Unwound all positions')
        print('=' * 55)
        print(f'Final balance [$]{self.amount:.2f}')
        performance = 100*(self.amount - self.initial_amount)/self.initial_amount
        print(f'Net Performance [%]{performance:.2f}')
        print(f'Trades Excecuted [#]{self.trades}')
        print('=' * 55)
        
    def strategy_var(self, price_bar):
        date = self.get_date(price_bar)

        lookback = 10
        window_data =self.model_data.loc[:date].iloc[-lookback:]
        if (pd.to_datetime(date) + timedelta(days=1)).weekday() >=5:
            forecast = self.model.forecast(window_data,3)
        else:
            forecast = self.model.forecast_one(window_data)

        delta = forecast - window_data[-1]    
        direction = np.sign(delta)
        if direction >=0:
            weights_market = np.sign(price_bar) * [1, 0]
        else:
            weights_market = np.sign(price_bar) * [0, 1]
        return weights_market

    def backtest(self):
        for date, price_bar in self.market_data.iterrows():
            price_bar = pd.DataFrame(price_bar).T
            
            absolute_strategy_allocation = self.strategy_var(price_bar)
            self.rebalance_positions(price_bar, absolute_strategy_allocation)
            
            self.days_traded += 1
            
        self.close_out(price_bar)

if __name__ == '__main__':         
    symbols = ["^OMX"]
    p = Portfolio(symbols, "2011-05-01", "2021-10-29", 2e4, verbose=True)
    p.backtest()

#TODO: Use mini-futures data to trade.