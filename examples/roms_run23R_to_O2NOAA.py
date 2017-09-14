import easy_coloc
import matplotlib.pylab as plt
import numpy as np

roms_grid      = '/Volumes/P1/ROMS-Inputs/CCS1/grid/CCS_7k_0-360_fred_grd.nc'
roms_data_june = '/Volumes/P7/ROMS/CCS1/CCS1-RD.NVOcobalt23R/interannual_monthly/CCS1-RD.NVOcobalt23R_avg_1996-2006-06_monthly.nc'
roms_data_july = '/Volumes/P7/ROMS/CCS1/CCS1-RD.NVOcobalt23R/interannual_monthly/CCS1-RD.NVOcobalt23R_avg_1996-2006-07_monthly.nc'
roms_data_aug  = '/Volumes/P7/ROMS/CCS1/CCS1-RD.NVOcobalt23R/interannual_monthly/CCS1-RD.NVOcobalt23R_avg_1996-2006-08_monthly.nc'
O2NOAA         = '../data/O2_bottom_trawl_NOAA_cleaned.csv'

# create easy_coloc object
roms2o2noaa     = easy_coloc.easy_coloc(roms_grid,from_global=False,coord_names=['lon_rho','lat_rho'],mask_var='mask_rho')
# define list of obs positions from text file for june to august
#lon_obs_june, lat_obs_june = roms2o2noaa.define_obs_position_from_text(O2NOAA,3,2,offset_line=1,separator=',',if_found=',6,')
#lon_obs_july, lat_obs_july = roms2o2noaa.define_obs_position_from_text(O2NOAA,3,2,offset_line=1,separator=',',if_found=',7,')
#lon_obs_aug,  lat_obs_aug  = roms2o2noaa.define_obs_position_from_text(O2NOAA,3,2,offset_line=1,separator=',',if_found=',8,')

lon_obs_june, lat_obs_june, o2_obs_june = roms2o2noaa.read_obs_data_from_text(O2NOAA,3,2,4,offset_line=1,separator=',',if_found=',6,')
lon_obs_july, lat_obs_july, o2_obs_july = roms2o2noaa.read_obs_data_from_text(O2NOAA,3,2,4,offset_line=1,separator=',',if_found=',7,')
lon_obs_aug,  lat_obs_aug,  o2_obs_aug  = roms2o2noaa.read_obs_data_from_text(O2NOAA,3,2,4,offset_line=1,separator=',',if_found=',8,')

lon_obs_june, lat_obs_june, depth_obs_june = roms2o2noaa.read_obs_data_from_text(O2NOAA,3,2,1,offset_line=1,separator=',',if_found=',6,')
lon_obs_july, lat_obs_july, depth_obs_july = roms2o2noaa.read_obs_data_from_text(O2NOAA,3,2,1,offset_line=1,separator=',',if_found=',7,')
lon_obs_aug,  lat_obs_aug,  depth_obs_aug  = roms2o2noaa.read_obs_data_from_text(O2NOAA,3,2,1,offset_line=1,separator=',',if_found=',8,')

# project model data onto observation space
out_june = roms2o2noaa.interpolate_model_onto_obs_space(lon_obs_june,lat_obs_june,roms_data_june,'o2',level=0,\
frame=0,spval=1.0e+15)
out_july = roms2o2noaa.interpolate_model_onto_obs_space(lon_obs_july,lat_obs_july,roms_data_july,'o2',level=0,\
frame=0,spval=1.0e+15)
out_aug = roms2o2noaa.interpolate_model_onto_obs_space(lon_obs_aug,lat_obs_aug,roms_data_aug,'o2',level=0,\
frame=0,spval=1.0e+15)

out_jja = np.concatenate((out_june,out_july,out_aug))

# write model data projected onto obs space into text file
#roms2o2noaa.write_to_file('roms_run23R_onto_o2noaa_june_1996-2006.txt',lon_obs_june,lat_obs_june,out_june)
#roms2o2noaa.write_to_file('roms_run23R_onto_o2noaa_july_1996-2006.txt',lon_obs_july,lat_obs_july,out_july)
#roms2o2noaa.write_to_file('roms_run23R_onto_o2noaa_aug_1996-2006.txt',lon_obs_aug,lat_obs_aug,out_aug)

# trick if we want to project on a season
# concat the obs points for all 3 months
lon_obs   = np.concatenate((lon_obs_june, lon_obs_july, lon_obs_aug))
lat_obs   = np.concatenate((lat_obs_june, lat_obs_july, lat_obs_aug))
o2_obs  = np.concatenate((o2_obs_june, o2_obs_july, o2_obs_aug))
depth_obs = np.concatenate((depth_obs_june, depth_obs_july, depth_obs_aug))

# project model bathy onto observation space
out_depth = roms2o2noaa.interpolate_model_onto_obs_space(lon_obs,lat_obs,roms_grid,'h',spval=1.0e+15)
# write model bathy projected onto obs space into text file
#roms2o2noaa.write_to_file('depth_roms_run23R_onto_o2noaa.txt',lon_obs,lat_obs,out_depth)

#----------plotting positions ---------------------
#plt.figure()
#plt.plot(lon_obs,lat_obs,'ko')
#plt.show()

out_jja = np.ma.masked_values(out_jja,1.0e+15)
out_depth = np.ma.masked_values(out_depth,1.0e+15)

# convert units for O2
out_jja = out_jja * 1035 * 22391.6 / 1000.0 # convert to mL/L

plt.figure()
plt.scatter(out_jja,-out_depth,c='k',alpha=0.3)
plt.scatter(o2_obs,-depth_obs,c='r',alpha=0.5)
#plt.xlim([0.,6.])
#plt.ylim([-500,0])
plt.show()
