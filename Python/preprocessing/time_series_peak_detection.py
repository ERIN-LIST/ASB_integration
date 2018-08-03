"""
    author: rkopeinig
    script: Peak detections
    description: Detect peaks from time series
    date: 08/03/2018
    version: 1.0
"""

# Import dependencies
import fire
import pandas as pd
from pytsa.preprocessing import peakdetect

# How to:
# python time_series_peak_detection.py --input 'input.csv' --output 'output/'


class TimeSeries(object):
    def __init__(self, input,output):
        self.input = input
        self.output = output
        self.time_series= pd.read_csv(self.input, index_col=0)
        self.time_series = self.time_series.reset_index()
        self.time_series['index'] = pd.to_datetime(self.time_series['index'])
        self.time_series = self.time_series.set_index('index')

        self.min_peaks, self.max_peaks = peakdetect(self.time_series['0'])
        self.save()

    def save(self):
        self.min_peaks.to_csv(self.output + 'min_peaks.csv')
        self.max_peaks.to_csv(self.output + 'max_peaks.csv')


if __name__ == '__main__':
  fire.Fire(TimeSeries)

