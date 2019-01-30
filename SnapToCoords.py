import pandas as pd
from scipy.spatial.distance import cdist
import os
from osgeo import gdal
import datetime as dt
import glob
from tqdm import tqdm
import time


df1 = pd.read_csv('../OrthoNormalWind/data/Matt_SPIDA_DATA.csv')
df2 = pd.read_csv('../AdHocs/HighPrioWeatherProj113018/NC_data_snapshot.csv')

source_latitude = 'Latitude'
source_longitude= 'Longitude'

target_latitude = 'lat'
target_longitude= 'long'

dfout = pd.DataFrame([])


def closest_point(point, points):
    #Returns closest point from a list of points.
    return points[cdist([point], points).argmin()]


def match_value(df, col1, x, col2):
    #Match value x from col1 row to value in col2.
    return df[df[col1] == x][col2].values[0]



df1['point'] = [(x, y) for x,y in zip(df1[source_latitude], df1[source_longitude])]
df2['point'] = [(x, y) for x,y in zip(df2[target_latitude], df2[target_longitude])]

df1['closest'] = [closest_point(x, list(df2['point'])) for x in df1['point']]

for feature in tqdm(['lat','lon']):
    df1[feature] = [match_value(df2, 'point', x, feature) for x in df1['closest']]


df1.to_csv("output.csv")

