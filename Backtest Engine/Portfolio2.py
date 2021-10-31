import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Portfolio:
    def __init__ (self, symbols, initial_capital, strategy, stop_loss= 0.65, ftc = 0, ptc = 0):   
        self.symbols = symbols
        self.capital = initial_capital
        self.initial_capital = initial_capital
        self.strategy = strategy
        self.stop_loss = stop_loss
        self.ftc = ftc
        self.ptc = ptc
        

        self.net_value = initial_capital
        self.positions = pd.DataFrame([np.zeros(len(symbols))], columns=symbols)
        self.trades = 0
        self.active = True

    def get_date(self, price_bar):
        date = str(price_bar.index.values[0])[:10]
        return date
    
    def get_net_wealth(self, price_bar):
        return (price_bar.reset_index(drop=True)*np.abs(self.positions)).sum(axis=1)[0] + self.capital
    
    def print_capital(self, price_bar):
        date = self.get_date(price_bar)
        print(f'{date} | current balance {self.capital:.2f}')
    
    def print_net_wealth(self, price_bar):
        date = self.get_date(price_bar)
        net_wealth = self.get_net_wealth(price_bar)
        print(f'{date} | current net wealthh {net_wealth:.2f}')

    def place_order(self, price_bar, symbol, units, order_type="MARKET"):
        date = self.get_date(price_bar)
        
        if units != 0:
            price = price_bar[symbol][0]

            self.capital -= units*price(1 + np.sign(units)*self.ptc) + self.ftc
            self.positions[symbol] += units
            self.trades += 1

    def place_orders(self, price_bar, symbols, units, order_type="MARKET"):
        for symbol in symbols:
            self.place_order(price_bar, symbol, units[symbol], order_type)

    def rebalance_portfolio(self, price_bar, weights):
        #Rebalance portfolios positions to mathch weights
        pass

    def close_out(self, price_bar):
        date = self.get_date(price_bar)
        self.place_orders(price_bar, self.positions.columns, self.positions )
        print(f'{date} | Closed out all positions')
        print('=' * 55)
        print(f'Final balance [$]{self.capital:.2f}')
        print(f'Final balance [$]{self.amount:.2f}')
        performance = 100*(self.amount - self.initial_amount)/self.initial_amount
        print(f'Net Performance [%]{performance:.2f}')
        print(f'Trades Excecuted [#]{self.trades}')
        print('=' * 55)

    def stop_loss_check(self, price_bar):
        net_wealth = self.get_net_wealth(price_bar)
        current_performance = net_wealth/self.initial_capital - 1
        if current_performance <= self.stop_loss:
            self.close_out(price_bar)
            self.active = False

    def step(self, price_bar):
        self.stop_loss_check(price_bar)

        if self.active:
            weights = self.strategy.step(price_bar)
            self.rebalance_portfolio(price_bar, weights)


if __name__ == "__main__":
    print("Test")