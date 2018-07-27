"""
    author: rkopeinig
    script: Workflow
    description: Workflow of retrieving time series from GeoJSON, aggregate, smooth and perform linear regression
    date: 07/27/2018
    version: 1.0
"""

# Import dependencies
import fire, datetime, requests, json
import pandas as pd
import geopandas as gpd
from dataclient.tsservice import get_curve, TSService
from dateutil import parser
from pytsa.preprocessing import savitz_golay
from sklearn import linear_model


# How to:
'''
python workflow.py --coverageId 'PROBAV_L3_S10_TOC_NDVI_333M' --start_date '2013-10-11T00:00Z' --end_date '2018-07-01T00:00Z' --geometry '../../../../data/ASB/geojson/ca.geojson' --aggregate 'M' --aggregate_function 'mean' --window 10 --polyorder 2 --output_folder '../../../../data/ASB/output/'
'''

class TimeSeries(object):
    def __init__(self, coverageId, start_date, end_date, geometry, aggregate, aggregate_function, window, polyorder, output_folder):
        self.coverageId = coverageId
        self.start_date = start_date
        self.end_date = end_date
        self.geometry = geometry
        self.aggregate = aggregate
        self.aggregate_function = aggregate_function
        self.output = output_folder
        self.time_series = self.get_time_series_from_geojson(self.coverageId,
                                                             self.geometry,
                                                             self.start_date,
                                                             self.end_date)

        self.time_series = self.time_series.resample(self.aggregate, how=self.aggregate_function)
        self.time_series = savitz_golay(self.time_series,window=window,polyorder=polyorder)

        self.lm = linear_model.LinearRegression()
        self.X = pd.DataFrame({'1': self.time_series[1],
                               '2': self.time_series[2],
                               '3': self.time_series[3]}, index=self.time_series.index)
        self.y = pd.DataFrame(self.time_series[0], index=self.time_series.index)

        model = self.lm.fit(self.X, self.y)
        predictions = self.lm.predict(self.X)
        self.result = pd.DataFrame(predictions, index=self.X.index)

        self.save()


    def get_time_series_from_geojson(self, coverage_id, geojson_path, start_date, end_date):
        with open(geojson_path) as f:
            data = json.load(f)

        geojson_dataframe = gpd.read_file(geojson_path)
        start_date = parser.parse(start_date)
        end_date = parser.parse(end_date)
        iterable = TSService().timeseries_async(coverage_id, geojson_dataframe, start_date, end_date)
        ts = []
        for i in iterable:
            ts.append(i)
        return pd.DataFrame(ts).T


    def save(self):
        self.time_series.to_csv(self.output+'time_series.csv')
        self.result.to_csv(self.output+'lin_reg_result.csv')

if __name__ == '__main__':
  fire.Fire(TimeSeries)

