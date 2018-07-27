"""
    author: rkopeinig
    script: Rolling Mean
    description: Rolling mean from time series
    date: 07/25/2018
    version: 1.0
"""

# Import dependencies
import fire
import pandas as pd
from pytsa.preprocessing import rolling_mean


# How to:
# python time_series_rolling_mean.py --input '../../../../data/ASB/input.csv' --window 10 --output '../../../../data/ASB/output/'


class TimeSeries(object):
    def __init__(self, input, window, output):
        self.input = input
        self.output = output
        self.time_series= pd.read_csv(self.input, index_col=0)
        self.time_series = self.time_series.reset_index()
        self.time_series['index'] = pd.to_datetime(self.time_series['index'])
        self.time_series = self.time_series.set_index('index')

        self.time_series = rolling_mean(self.time_series, window)
        self.save()

    def save(self):
        self.time_series.to_csv(self.output+'rolling_mean.csv')


if __name__ == '__main__':
  fire.Fire(TimeSeries)

