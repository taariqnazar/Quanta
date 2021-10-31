import numpy as np
import pandas as pd

from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.vector_ar.var_model import VAR

import yfinance as yf

class TS_Model():
    def __init__(self, params, train_data):
        """
        params: (p, i, q) order of time series
        train_data: data to train the model to.
        """
        self.params = params
        self.data = train_data
        self.init_model()

    def init_model(self):
        model = ARIMA(self.data.values, order = self.params)
        self.model = model.fit()

    def forecast(self, data,steps):
        forecast = self.model.apply(data).forecast(steps).values[0]
        return forecast
    
    def forecast_one(self, data):
        return self.forecast(data, 1)

class TS_Ensemble():
    def __init__(self, params_list, train_data):
        self.params_list = params_list
        self.data = train_data
        self.init_model()
    
    def init_model(self):
        models = {}
        for i, params in self.params_list.iterrows():
            model = TS_Model(params, self.data)
            models[i] = model
        self.models = models
    
    def forecast(self, data, steps):
        forecasts = []
        for i, model in self.models.items():
            forecast = model.forecast(data, steps)
            forecasts.append(forecast)

        return np.mean(forecasts)

    def forecast_one(self, data):
        return self.forecast(data, 1)


if __name__ == '__main__':
    """
                    [1, 1, 0],
                    [2, 1, 3],
                    [4, 1, 2],
                    [3, 1, 4]
    """
    best_params = pd.DataFrame([[0, 1, 0],
       [0, 1, 1],
       [1, 1, 0],
       [2, 1, 3],
       [4, 1, 2],
       [3, 1, 4]], columns=[['p', 'i', 'q']])
    
    train_data = yf.Ticker('^OMX').history(start="2011-05-01")[:'2021-01-29']['Close'].ffill()
    ensemble = TS_Ensemble(best_params, train_data)

    test_data = pd.DataFrame([1653.2800293 , 1652.57995605, 1670.20996094, 1677.18994141,
       1682.86999512, 1697.91003418, 1724.35998535, 1728.2199707 ], index = ['2019-10-11', '2019-10-14', '2019-10-15', '2019-10-16',
               '2019-10-17', '2019-10-18', '2019-10-21', '2019-10-22'])
    f = ensemble.forecast_one(test_data) 
    print(f)