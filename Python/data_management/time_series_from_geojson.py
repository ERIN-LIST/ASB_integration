"""
    author: rkopeinig
    script: Time Series from GeoJSON
    description: Retrieving time series from GeoJSON
    date: 06/26/2018
    version: 1.0
"""

# Import dependencies
import fire, datetime, requests, json
import pandas as pd
import geopandas as gpd
from dataclient.tsservice import get_curve, TSService
from dateutil import parser


# How to:
# python time_series_from_geojson.py --coverageId 'PROBAV_L3_S10_TOC_NDVI_333M' --start_date '2013-10-11T00:00Z' --end_date '2018-07-01T00:00Z' --geometry '../../../../data/ASB/geojson/ca.geojson' --output '../../../../data/ASB/output/'

class TimeSeries(object):
    def __init__(self, coverageId, start_date, end_date, geometry, output):
        self.coverageId = coverageId
        self.start_date = start_date
        self.end_date = end_date
        self.geometry = geometry
        self.output = output
        self.time_series = self.get_time_series_from_geojson(self.coverageId,
                                                             self.geometry,
                                                             self.start_date,
                                                             self.end_date)
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

if __name__ == '__main__':
  fire.Fire(TimeSeries)

