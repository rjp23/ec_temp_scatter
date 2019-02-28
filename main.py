import datetime
from IPython import embed
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import pandas as pd
import scipy as sp
from netCDF4 import num2date, date2num
from netCDF4 import Dataset, MFDataset
import glob
import os
import dask
import xarray
import cartopy.feature as cfeature
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from shapely.geometry import Point, Polygon
from dateutil.parser import parse
import matplotlib.dates as mdates
from matplotlib import ticker
from datetime import timedelta
import seaborn as sns

import hvplot
import hvplot.pandas
import holoviews as hv
from holoviews import opts
hv.extension('bokeh', 'matplotlib', width="100")
import hvplot.xarray
from bokeh.models import Slope


ds = xarray.open_dataset('ds_transcom_merged.nc')

#change names back from bytestrings to strings (python2->3 thing?)
region_coords = [transcom_region.decode("utf-8") for transcom_region in ds.transcom.values]
model_coords = [model.decode("utf-8") for model in ds.model_id.values]
ds = ds.assign_coords(transcom=region_coords, model_id=model_coords)

model_colors_dict = {'ACCESS1-0': ('purple', 'o'),
                     'ACCESS1-3': ('lilac', 's'),
                     'BNU-ESM': ('beige', 'o'),
                     'CESM1-CAM5': ('fern', 'o'),
                     'CESM1-FASTCHEM': ('dark yellow green', 's'),
                     'CESM1-WACCM': ('dark sage', '^'),
                     'CMCC-CM': ('muted pink', 's'),
                     'CMCC-CMS': ('coral pink', 'o'),
                     'CanESM2': ('cinnamon', 'o'),
                     'FIO-ESM': ('butterscotch', 'o'),
                     'GFDL-CM3': ('frog green', 'o'),
                     'GFDL-ESM2G': ('dark mint', 's'),
                     'GISS-E2-H-CC': ('deep orange', 'o'),
                     'GISS-E2-R': ('pastel orange', '^'),
                     'GISS-E2-R-CC': ('rusty orange', 's'),
                     'HadCM3': ('muted blue', 'o'),
                     'HadGEM2-CC': ('blueberry', 's'),
                     'HadGEM2-ES': ('bluish', '^'),
                     'IPSL-CM5A-LR': ('dull red', 'o'),
                     'IPSL-CM5A-MR': ('vermillion', 's'),
                     'IPSL-CM5B-LR': ('faded red', '^'),
                     'MPI-ESM-LR': ('pale teal', 'o'),
                     'MPI-ESM-MR': ('teal blue', 's'),
                     'MPI-ESM-P': ('teal green', '^'),
                     'NorESM1-M': ('light purple', 's'),
                     'NorESM1-ME': ('lavender', 'o'),
                     'bcc-csm1-1': ('clay', 's'),
                     'bcc-csm1-1-m': ('burnt umber', 'o'),
                     'inmcm4': ('golden yellow', 'o'),
                     'CCSM4': ('dark brown', 'o'),
                     'MRI-CGCM3': ('deep violet', 'o'),
                     'MRI-ESM1': ('dusky purple', 's'),
                     'MIROC5': ('neon purple', 'o'),
                     'MIROC-ESM-CHEM': ('blue violet', 's'),
                     'MIROC-ESM': ('violet blue', '^'),
                     'GFDL-ESM2M': ('kelly green', 'o')}


transcom_region_ids_dict = {'global_land': {'name':'Global Land', 'id':'0'},
                            'nam_bor': {'name':'North American Boreal',  'id':'1'},
                            'nam_temp': {'name':'North American Temperate', 'id':'2'},
                            'sam_trop': {'name':'South American Tropical', 'id':'3'},
                            'sam_temp': {'name':'South American Temperate', 'id':'4'},
                            'naf': {'name':'Northern Africa', 'id':'5'},
                            'saf': {'name':'Southern Africa', 'id':'6'},
                            'eur_bpr': {'name':'Eurasian Boreal', 'id':'7'},
                            'eur_temp': {'name':'Eurasian Temperate', 'id':'8'},
                            'trop_asia': {'name':'Tropical Asia', 'id':'9'},
                            'aus': {'name':'Australia', 'id':'10'},
                            'eur': {'name':'Europe', 'id':'11'},
                            'other': {'name':'Other', 'id':'100'},
                            }


region_dict  = {    'global': {'name': 'Global', 'box': [0,360,-90,90]},
                    'global_ex_ant': {'name': 'Global (Excluding Antarctica)', 'box': [0,360,-60,90]},
                    '60S_60N': {'name': '60 North to 60 South', 'box': [0,360,-60,60]},
                    'nhem': {'name': 'Northern Hemisphere', 'box': [0,360,0,90]},
                    'shem': {'name': 'Southern Hemisphere', 'box': [0,360,-90,0]},
                    'tropics': {'name': 'Tropics', 'box': [0,360,-30,30]},
                    'stropics': {'name': 'South Tropics', 'box': [0,360,-30,0]},
                    'ntropics': {'name': 'North Tropics', 'box': [0,360,0,30]},
                    'pantanal': {'name': 'Pantanal', 'box': [290, 308, -21, 10]},
                    'parana': {'name': 'Parana', 'box': [295, 308, -35, -25]},
                    'wamazon': {'name': 'West Amazon', 'box': [280, 300, -8, 5]},
                    'eamazon': {'name': 'East Amazon', 'box': [300, 320, -8, 5]},
                    'yucatan': {'name': 'Yucatan', 'box': [263,275, 15, 23]},
                    'eus': {'name': 'East US', 'box': [263, 290, 25, 40]},
                    'sudd': {'name': 'Sudd', 'box': [25, 40, 3, 17]},
                    'congo': {'name': 'Congo', 'box': [15, 25, -4, 4]},
                    'safrica': {'name': 'Southern Africa', 'box': [15, 33, -22, -8]},
                    'china': {'name': 'China', 'box': [110, 125, 25, 40]},
                    'seasia': {'name': 'S.E. Asia', 'box': [90, 110, 8, 20]},
                    'indonesia': {'name': 'Indonesia', 'box': [95, 126, -10, 8]},
                    'papua': {'name': 'Papua', 'box': [131, 150, -10, -1]},
                    'indogangetic': {'name': 'Indo-Gangetic', 'box': [66, 96, 22, 34]},
                    'naustralia': {'name': 'N. Australia', 'box': [125, 150, -20, -11]},
                    'seaustralia': {'name': 'S.E. Australia', 'box': [140, 155, -40, -25]},
                }


region_dict.update(transcom_region_ids_dict)


regions = []
for region in ds.transcom.values:

    '''
    if region == 'other':
        continue
    '''

    regions.append(region_dict[region]['name'])


model_ids = ds.model_id.values

model_colors = [model_colors_dict[key][0] for key in model_ids]

model_palette = sns.xkcd_palette(model_colors)
sns.set_palette(model_palette)

model_cmap = matplotlib.colors.ListedColormap(model_palette)

ds = ds.assign_coords(transcom=regions).drop(['day_of_month', 'height'])
ds = ds.rename({'model_id':'Model Name', 'transcom':'Region'})



colors = np.arange(36)
y, x = np.meshgrid(colors, np.arange(37))
x = np.ravel(x)

scat = ds.hvplot.scatter(x='tas_change', y='tsl_change', groupby='Region', c=x, height=900, width=900)

scat = scat.opts(opts.Scatter(xlabel='Air Temperature Change (1861-2005)', ylabel='Soil Temperature Change (1861-2005)'))

scat = scat.opts(opts.Scatter(cmap=model_cmap, marker='o', line_color="black", size=15,fill_alpha=0.8))
scat = scat.opts(fontsize={'title': 16, 'labels': 16, 'xticks': 12, 'yticks': 12})
scat = scat.opts(xlim=(0,2), ylim=(0,2), legend_offset=(15,-10), toolbar=None)




def hook(plot, element):

    print('plot.state:   ', plot.state)
    print('plot.handles: ', sorted(plot.handles.keys()))
    #  plot.handles['xaxis'].axis_label_text_color = 'red'
    #  plot.handles['yaxis'].axis_label_text_color = 'blue'
    #  plot.state.legend[0].location = (50,0)
    plot.state.background_fill_color = "ghostwhite"
    plot.state.background_fill_alpha = 0.8
    plot.state.outline_line_color = "black"
    plot.state.legend[0].border_line_color = "black"
    plot.state.legend[0].background_fill_color = "ghostwhite"
    plot.state.legend[0].background_fill_alpha = 0.8
    #plot.state.grid[0].grid_line_color = "white"
    #plot.state.grid[0].grid_line_width = 4
    plot.state.legend[0].label_text_font_size = "12pt"
    #plot.state.legend[0].label_height = 30
    plot.state.legend[0].glyph_height = 30
    plot.state.legend[0].glyph_width = 30
    plot.state.legend[0].spacing = -8

    x = element.dimension_values('tas_change')
    y = element.dimension_values('tsl_change')

    find_nans = np.isfinite(x) & np.isfinite(y)

    x = x[find_nans]
    y = y[find_nans]


    par = np.polyfit(x, y, 1, full=True)
    gradient=par[0][0]
    y_intercept=par[0][1]

    if 'slope' in plot.handles:
        slope = plot.handles['slope']
        slope.gradient = gradient
        slope.y_intercept = y_intercept
    else:
        slope = Slope(gradient=gradient, y_intercept=y_intercept,
              line_color='orange', line_dash='dashed', line_width=3.5)
        plot.handles['slope'] = slope
        plot.state.add_layout(slope)




# renders object so it can be explored
# scat_rend = hv.render(scat)

scat = scat.opts(hooks=[hook])
hvplot.show(scat)



