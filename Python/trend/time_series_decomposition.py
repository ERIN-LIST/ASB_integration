"""
    author: rkopeinig
    script: Seasonal Decomposition
    description: Decompose a time series
    date: 07/25/2018
    version: 1.0
"""

# Import dependencies
import fire
import pandas as pd
from pytsa.trend import seasonal_decomposition


# How to:
# python time_series_decomposition.py --input '../../../../data/ASB/input.csv' --freq 10 --output '../../../../data/ASB/output/'


class TimeSeries(object):
    def __init__(self, input, freq, output):
        self.input = input
        self.output = output
        self.freq = freq
        self.time_series= pd.read_csv(self.input, index_col=0)
        self.time_series = self.time_series.reset_index()
        self.time_series['index'] = pd.to_datetime(self.time_series['index'])
        self.time_series = self.time_series.set_index('index')

        self.res = seasonal_decomposition(self.time_series['0'],model='additive',freq=freq)
        self.result= pd.DataFrame({'trend':self.res.trend,
                                   'resid': self.res.resid,
                                   'seasonal':self.res.seasonal},index=self.time_series.index)
        self.save()

    def save(self):
        self.result.to_csv(self.output+'decomposition.csv')


if __name__ == '__main__':
  fire.Fire(TimeSeries)

