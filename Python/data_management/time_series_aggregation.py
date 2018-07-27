"""
    author: rkopeinig
    script: Aggregate Time Series
    description: Aggregating time series retrieved from GeoJSON
    date: 06/26/2018
    version: 1.0
"""

# Import dependencies
import fire
import pandas as pd


# How to:
# python time_series_aggregation.py --input '../../../../data/ASB/input.csv' --output ''../../../../data/ASB/output/' --aggregate='Q' --aggregate_function='mean'

class TimeSeries(object):
    def __init__(self, input, output, aggregate='M', aggregate_function='mean'):
        self.input = input
        self.output = output
        self.aggregate = aggregate
        self.aggregate_function = aggregate_function
        self.time_series= pd.read_csv(self.input, index_col=0)
        self.time_series = self.time_series.reset_index()
        self.time_series['index'] = pd.to_datetime(self.time_series['index'])
        self.time_series = self.time_series.set_index('index')
        self.time_series=self.time_series.resample(self.aggregate, how = self.aggregate_function)
        self.save()

    def save(self):
        self.time_series.to_csv(self.output+'result_aggregated.csv')


if __name__ == '__main__':
  fire.Fire(TimeSeries)

