import easy_coloc
import matplotlib.pylab as plt

roms_grid = '/Users/raphael/STORAGE/ROMS/GRIDS/CCS_7k_0-360_fred_grd.nc'
roms_data = '/Users/raphael/STORAGE/ROMS/CCS1-RD.NVOcobalt22S_avg_1995-01-17T00:00:00.nc'
seawifs_clim = '../data/seawifs_december.nc'

roms2seawifs = easy_coloc.easy_coloc(roms_grid,from_global=False,coord_names=['lon_rho','lat_rho'],mask_var='mask_rho')
lon_obs, lat_obs, data_obs, jindex, iindex = roms2seawifs.define_obs_position_from_gridded(seawifs_clim,'chl',frame=0)
data_model = roms2seawifs.interpolate_model_onto_obs_space(lon_obs,lat_obs,roms_data,'temp',level=-1,frame=0,spval=1.0e+15)
out_2d = roms2seawifs.reshape_interpolated_data(jindex,iindex,data_model)

roms2seawifs.write_to_file('obs.txt',lon_obs,lat_obs,data_obs)
roms2seawifs.write_to_file('model.txt',lon_obs,lat_obs,data_model)


#plt.figure()
##plt.plot(lon_obs,lat_obs,'ko')
#plt.pcolor(roms2seawifs.lon_gridded_2d,roms2seawifs.lat_gridded_2d,out_2d); plt.colorbar()
#plt.show()
