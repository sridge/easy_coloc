import easy_coloc
import matplotlib.pylab as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import pandas as pd

roms_grid = '/Volumes/P1/ROMS-Inputs/CCS1/grid/CCS_7k_0-360_fred_grd.nc'
roms_data = '/Volumes/P4/workdir/raphael/analysis_CCS1-Cobalt/CCS1-RD.NVOcobalt23R-MEAN/interannual_monthly/CCS1-RD.NVOcobalt23R_dia_1996-2006-JJA_season.nc'
copepod_JJA = '/Volumes/P1/Data/Copepod/originals/data/copepod-2012__cmass-m15-qtr.csv'

# create easy_coloc object
roms2copepod     = easy_coloc.easy_coloc(roms_grid,from_global=False,coord_names=['lon_rho','lat_rho'],mask_var='mask_rho')
#  define list of obs positions from text file
lon_obs, lat_obs = roms2copepod.define_obs_position_from_text(copepod_JJA,0,1,offset_line=1,separator=',')
# project model data onto observation space
out              = roms2copepod.interpolate_model_onto_obs_space(lon_obs,lat_obs,roms_data,'mesozoo_200',frame=0,spval=1.0e+15)

# write model data projected onto obs space into text file
roms2copepod.write_to_file('roms_REF_JJA_1996-2006_onto_copepod_JJA.txt',lon_obs,lat_obs,out)

#---------- plotting results ---------------------

def setup_map():
	bmap = Basemap(projection='cyl',llcrnrlat=18,urcrnrlat=51,\
	                                llcrnrlon=219-360,urcrnrlon=251-360,resolution='l')
	parallels = np.arange(20.,60.,10.)
	bmap.drawparallels(parallels,labels=[True,False,False,True])
	meridians = np.arange(220.,260.,10.)
	bmap.drawmeridians(meridians,labels=[True,False,False,True])
	bmap.drawcoastlines()
	return bmap

# read from text file
mesozoo_roms = pd.read_csv('./roms_REF_JJA_1996-2006_onto_copepod_JJA.txt',header=None, names=['lon','lat','data'])
mesozoo_copepod = pd.read_csv('/Volumes/P1/Data/Copepod/originals/data/copepod-2012__cmass-m15-qtr.csv',usecols=[0,1,3])

# filter missing value
mesozoo_roms_flt = mesozoo_roms[mesozoo_roms['data'] != 1.000000e+15]
mesozoo_copepod_flt = mesozoo_copepod[mesozoo_roms['data'] != 1.000000e+15]

plt.figure()
m = setup_map()
sc = m.scatter(mesozoo_roms_flt['lon'].values, mesozoo_roms_flt['lat'].values,\
c=mesozoo_roms_flt['data'].values/200,vmin=0,vmax=14)
plt.colorbar(sc)
plt.title('ROMS')

plt.figure()
m = setup_map()
sc = m.scatter(mesozoo_copepod_flt['Longitude'].values, mesozoo_copepod_flt['Latitude'].values,\
c=mesozoo_copepod_flt['Total Carbon Mass (mg-C/m3)'].values,vmin=0,vmax=14)
plt.colorbar(sc)
plt.title('Copepod')

plt.show()
