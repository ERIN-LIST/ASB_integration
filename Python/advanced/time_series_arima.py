"""
    author: rkopeinig
    script: ARIMA
    description: ARIMA on time series retrieved from csv
    date: 07/25/2018
    version: 1.0
"""

# Import dependencies
import fire
import pandas as pd
from pytsa.advanced import arima_model

# How to:
# python time_series_arima.py --input '../../../../data/ASB/input.csv' --output '../../../../data/ASB/output/'

class TimeSeries(object):
    def __init__(self, input, output):
        self.input = input
        self.output = output
        self.time_series= pd.read_csv(self.input, index_col=0)
        self.time_series = self.time_series.reset_index()
        self.time_series['index'] = pd.to_datetime(self.time_series['index'])
        self.time_series = self.time_series.set_index('index')

        RSS,log_series_diff,arima = arima_model(self.time_series['0'])
        print(RSS)
        self.result = pd.DataFrame({'arima_fittedvalues':arima.fittedvalues, 'log_series_diff':log_series_diff})
        self.save()

    def save(self):
        self.result.to_csv(self.output+'result_arima.csv')


if __name__ == '__main__':
  fire.Fire(TimeSeries)

