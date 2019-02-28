import xarray
import hvplot
import holoviews as hv
from holoviews import opts
hv.extension('bokeh', 'matplotlib', width="100")
import hvplot.xarray

renderer = hv.renderer('bokeh')

ds = xarray.open_dataset('data/ds_transcom_merged.nc')

#change names back from bytestrings to strings (python2->3 thing?)
region_coords = [transcom_region.decode("utf-8") for transcom_region in ds.transcom.values]
model_coords = [model.decode("utf-8") for model in ds.model_id.values]
ds = ds.assign_coords(transcom=region_coords, model_id=model_coords).drop(['day_of_month', 'height'])
ds = ds.rename({'model_id':'Model Name', 'transcom':'Region'})

scat = ds.hvplot.scatter(x='tas_change', y='tsl_change', groupby='Region', height=900, width=900)

doc = renderer.server_doc(scat)doc.title = 'HoloViews App'
