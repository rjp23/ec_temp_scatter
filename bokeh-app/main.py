import xarray
import hvplot
import holoviews as hv
from holoviews import opts
import hvplot.xarray
import hvplot.pandas
from os.path import join, dirname
import numpy as np

#air_ds = xarray.tutorial.open_dataset('air_temperature').load()

renderer = hv.renderer('bokeh')



ds = xarray.open_dataset('bokeh-app/data/ds_transcom_merged.nc')


#change names back from bytestrings to strings (python2->3 thing?)
region_coords = [transcom_region.decode("utf-8") for transcom_region in ds.transcom.values]
model_coords = [model.decode("utf-8") for model in ds.model_id.values]
ds = ds.assign_coords(transcom=region_coords, model_id=model_coords).drop(['day_of_month', 'height'])
#ds = ds.isel(model_id=slice(0,10))
#ds = ds.isel(transcom=slice(0,10))


#air_ds_small = air_ds.isel(lat=0).isel(time=slice(0,10), lon=slice(0,10))

#air_ds_small_new_coords = air_ds_small.assign_coords(transcom=region_coords[0:10], model_id=model_coords[0:10])
#ds = ds.rename({'model_id':'Model Name', 'transcom':'Region'})
#scat = air_ds_small.hvplot.scatter(x='time', y='air', groupby='lon', height=600, width=600)

scat = ds.hvplot.scatter(x='tas_change', y='tsl_change', groupby='transcom', height=600, width=600)


#hvplot.show(scat)
doc = renderer.server_doc(scat)
doc.title = 'HoloViews App'



