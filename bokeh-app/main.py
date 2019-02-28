import datetime
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import scipy as sp
from netCDF4 import num2date, date2num
from netCDF4 import Dataset, MFDataset
import glob
import os
import dask
import xarray
from dateutil.parser import parse
import matplotlib.dates as mdates
from matplotlib import ticker
from datetime import timedelta
import seaborn as sns
import hvplot
import holoviews as hv
from holoviews import opts
hv.extension('bokeh', 'matplotlib', width="100")
import hvplot.xarray


ds = xarray.open_dataset('data/ds_transcom_merged.nc')

#change names back from bytestrings to strings (python2->3 thing?)
region_coords = [transcom_region.decode("utf-8") for transcom_region in ds.transcom.values]
model_coords = [model.decode("utf-8") for model in ds.model_id.values]
ds = ds.assign_coords(transcom=region_coords, model_id=model_coords)

ds = ds.assign_coords(transcom=regions).drop(['day_of_month', 'height'])
ds = ds.rename({'model_id':'Model Name', 'transcom':'Region'})

ds.hvplot.scatter(x='tas_change', y='tsl_change', groupby='Region', height=900, width=900)

