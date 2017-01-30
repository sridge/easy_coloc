import easy_coloc
import matplotlib.pylab as plt
import numpy as np

roms_grid      = '/Users/raphael/STORAGE/ROMS/GRIDS/CCS_7k_0-360_fred_grd.nc'
roms_data_june = '/Users/raphael/STORAGE/ROMS/CCS1-RD.NVOcobalt22S_avg_1995-01-17T00:00:00.nc'
roms_data_july = '/Users/raphael/STORAGE/ROMS/CCS1-RD.NVOcobalt22S_avg_1995-01-17T00:00:00.nc'
roms_data_aug  = '/Users/raphael/STORAGE/ROMS/CCS1-RD.NVOcobalt22S_avg_1995-01-17T00:00:00.nc'
O2NOAA         = '/Users/raphael/Dropbox/CCS_ROMS/O2_bottom_NOAA/O2_bottom_trawl_NOAA_cleaned.csv'

# create easy_coloc object
roms2o2noaa     = easy_coloc.easy_coloc(roms_grid,from_global=False,coord_names=['lon_rho','lat_rho'],mask_var='mask_rho')
# define list of obs positions from text file for june to august
lon_obs_june, lat_obs_june = roms2o2noaa.define_obs_position_from_text(O2NOAA,3,2,offset_line=1,separator=',',if_found=',6,')
lon_obs_july, lat_obs_july = roms2o2noaa.define_obs_position_from_text(O2NOAA,3,2,offset_line=1,separator=',',if_found=',7,')
lon_obs_aug,  lat_obs_aug  = roms2o2noaa.define_obs_position_from_text(O2NOAA,3,2,offset_line=1,separator=',',if_found=',8,')

# project model data onto observation space
out_june = roms2o2noaa.interpolate_model_onto_obs_space(lon_obs_june,lat_obs_june,roms_data_june,'o2',level=0,\
frame=0,spval=1.0e+15)
out_july = roms2o2noaa.interpolate_model_onto_obs_space(lon_obs_july,lat_obs_july,roms_data_july,'o2',level=0,\
frame=0,spval=1.0e+15)
out_aug = roms2o2noaa.interpolate_model_onto_obs_space(lon_obs_aug,lat_obs_aug,roms_data_aug,'o2',level=0,\
frame=0,spval=1.0e+15)

# write model data projected onto obs space into text file
roms2o2noaa.write_to_file('roms_onto_o2noaa_june.txt',lon_obs_june,lat_obs_june,out_june)
roms2o2noaa.write_to_file('roms_onto_o2noaa_july.txt',lon_obs_july,lat_obs_july,out_july)
roms2o2noaa.write_to_file('roms_onto_o2noaa_aug.txt',lon_obs_aug,lat_obs_aug,out_aug)

# trick if we want to project on a season
# concat the obs points for all 3 months
lon_obs = np.concatenate((lon_obs_june, lon_obs_july, lon_obs_aug))
lat_obs = np.concatenate((lat_obs_june, lat_obs_july, lat_obs_aug))
# project model bathy onto observation space
out     = roms2o2noaa.interpolate_model_onto_obs_space(lon_obs,lat_obs,roms_grid,'h',spval=1.0e+15)
# write model bathy projected onto obs space into text file
roms2o2noaa.write_to_file('bathy_roms_onto_o2noaa.txt',lon_obs,lat_obs,out)

#----------plotting positions ---------------------
#plt.figure()
#plt.plot(lon_obs,lat_obs,'ko')
#plt.show()

