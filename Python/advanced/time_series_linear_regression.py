"""
    author: rkopeinig
    script: Linear Regression
    description: Linear Regression on time series retrieved from csv
    date: 07/26/2018
    version: 1.0
"""

# Import dependencies
import fire
import pandas as pd
from sklearn import linear_model


# How to:
# python time_series_linear_regression.py --input '../../../../data/ASB/input.csv' --output '../../../../data/ASB/output/'


class TimeSeries(object):
    def __init__(self, input, output):
        self.input = input
        self.output= output
        self.time_series = pd.read_csv(self.input, index_col=0)
        self.time_series = self.time_series.reset_index()
        self.time_series['index'] = pd.to_datetime(self.time_series['index'])
        self.time_series = self.time_series.set_index('index')

        self.lm = linear_model.LinearRegression()
        self.X = pd.DataFrame({'1':self.time_series['1'],
                               '2':self.time_series['2'],
                               '3':self.time_series['3']},index=self.time_series.index)
        self.y = pd.DataFrame(self.time_series['0'],index=self.time_series.index)

        model = self.lm.fit(self.X, self.y)
        predictions = self.lm.predict(self.X)
        self.result = pd.DataFrame(predictions,index=self.X.index)
        self.save()

    def save(self):
        self.result.to_csv(self.output+'linear_reg.csv')


if __name__ == '__main__':
  fire.Fire(TimeSeries)

