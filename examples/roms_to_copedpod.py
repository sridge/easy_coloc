import easy_coloc
import matplotlib.pylab as plt

roms_grid = '/Users/raphael/STORAGE/ROMS/GRIDS/CCS_7k_0-360_fred_grd.nc'
roms_data = '/Users/raphael/STORAGE/ROMS/CCS1-RD.NVOcobalt22S_avg_1995-01-17T00:00:00.nc'
copepod_JJA = '/Users/raphael/TOOLS/workspace-raphael.git/data_processing/copepod_nvo/copepod-2012_cmass_20160729.csv'

# create easy_coloc object
roms2copepod     = easy_coloc.easy_coloc(roms_grid,from_global=False,coord_names=['lon_rho','lat_rho'],mask_var='mask_rho')
#  define list of obs positions from text file
lon_obs, lat_obs = roms2copepod.define_obs_position_from_text(copepod_JJA,0,1,offset_line=1,separator=',',if_found='JJA')
# project model data onto observation space
out              = roms2copepod.interpolate_model_onto_obs_space(lon_obs,lat_obs,roms_data,'temp',level=-1,frame=0,spval=1.0e+15)

# write model data projected onto obs space into text file
roms2copepod.write_to_file('roms_onto_copepod.txt',lon_obs,lat_obs,out)

#----------plotting positions ---------------------
#plt.figure()
#plt.plot(lon_obs,lat_obs,'ko')
#plt.show()

