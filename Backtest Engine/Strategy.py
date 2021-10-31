import pandas as pd
import numpy as np

from abc import ABC, abstractmethod
from models import TS_Ensemble

class Strategy(ABC):

    @abstractmethod
    def step(self, price_bar):
        raise NotImplementedError("step() method is not implemented")
    
    def get_date(self,price_bar):
        date = str(price_bar.index.values[0])[:10]
        return date

class TS_Forecast(Strategy):
    def __init__(self, params_list, data):
        self.model = TS_Ensemble(params_list, data)
        self.data = data

    def update_data(self, price_bar):
        new_data = price_bar[self.data.columns]
        self.data = self.data.append(new_data)

    def step(self, price_bar):
        date = self.get_date(price_bar)

        lookback = 10
        window_data =self.data.loc[:date].iloc[-lookback:]
        forecast = self.model.forecast_one(window_data)
        delta = forecast - window_data[-1]    
        direction = np.sign(delta)

        if direction >=0:
            weights = np.sign(price_bar) * [1, 0]
        else:
            weights = np.sign(price_bar) * [0, 1]
        return weights