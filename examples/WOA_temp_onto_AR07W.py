from easy_coloc import lib_easy_coloc
import xarray as xr
import pandas as pd
import cartopy as cart
import matplotlib.pylab as plt
from matplotlib import cm

# load stations information from csv file
ar07w = pd.read_csv('../easy_coloc/test/test_files/AR07W_stations.txt',skipinitialspace=True)

# load gridded dataset
ds = xr.open_dataset('../easy_coloc/test/test_files/woa_labrador.nc',decode_times=False)

# create source grid and target section objects
# this requires lon,lat from stations and the source grid dataset containing lon,lat
proj = lib_easy_coloc.projection(ar07w['lon'].values,ar07w['lat'].values,grid=ds,
                                 from_global=False)

# run the projection on the WOA analyzed temperature (t_an)
fld = proj.run(ds['t_an'])


plt.figure(figsize=[6,6])
m = plt.axes(projection=cart.crs.PlateCarree())
m.scatter(ar07w['lon'].values,ar07w['lat'].values,c=fld[0,0,0,:])
m.coastlines()
m.add_feature(cart.feature.LAND, facecolor='0.75')
m.set_extent([-75, -35, 35, 65], crs=cart.crs.PlateCarree())
gl = m.gridlines(draw_labels=True)

plt.figure(figsize=[6,6])
plt.contourf(ar07w['lat'].values,-ds['depth'],fld[0,0,:,:],30,cmap=cm.gist_ncar)
plt.colorbar()
plt.title('WOA temperature at AR07W section')
plt.show()
