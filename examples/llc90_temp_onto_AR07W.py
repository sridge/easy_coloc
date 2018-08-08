from easy_coloc import lib_easy_coloc
import xarray as xr
import pandas as pd
import cartopy as cart
import matplotlib.pylab as plt
from matplotlib import cm
import xmitgcm
import numpy as np

# load stations information from csv file
ar07w = pd.read_csv('../data/AR07W_stations.txt',skipinitialspace=True)

# load gridded dataset
ds = xmitgcm.open_mdsdataset('../data/global_oce_llc90/',prefix=['T'],geometry='llc')

# quick look at the input data, the face we need for AR07W is #10
#ds['T'].sel(face=10,k=0,time=8).plot(cmap=cm.gist_ncar); plt.show()

# create source grid and target section objects
# this requires lon,lat from stations and the source grid dataset containing lon,lat
# here subsetting face 10 of ds and passing the names of lon/lat coords in ds
proj = lib_easy_coloc.projection(ar07w['lon'].values,ar07w['lat'].values,grid=ds.sel(face=10),
                                 coord_names=['XC','YC'],from_global=False)

# run the projection on the WOA analyzed temperature (t_an)
fld = proj.run(ds['T'].sel(face=10),mask_value=0)

plt.figure(figsize=[6,6])
m = plt.axes(projection=cart.crs.PlateCarree())
m.scatter(ar07w['lon'].values,ar07w['lat'].values,c=fld[0,0,:])
m.coastlines()
m.add_feature(cart.feature.LAND, facecolor='0.75')
m.set_extent([-75, -35, 35, 65], crs=cart.crs.PlateCarree())
gl = m.gridlines(draw_labels=True)

plt.figure(figsize=[6,6])
plt.contourf(ar07w['lat'].values,ds['Z'],np.ma.masked_values(fld[0,:,:],0),30,cmap=cm.gist_ncar)
plt.colorbar()
plt.title('ECCO temperature at AR07W section')
plt.show()
