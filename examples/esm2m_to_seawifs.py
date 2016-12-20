import easy_coloc
import matplotlib.pylab as plt

esm2m_grid = '/Users/raphael/STORAGE/COBALT/GFDL_CM2.1_grid.nc'
esm2m_data = '/Users/raphael/STORAGE/COBALT/ocean_cobalt_tracers.1988-2007.01_12.nc'
seawifs_clim = '../data/seawifs_december.nc'

esm2m2seawifs = easy_coloc.easy_coloc(esm2m_grid,from_global=True,coord_names=['geolon_t','geolat_t'],mask_var='kmt',mask_value=-1.0e20)
lon_obs, lat_obs, data_obs, jindex, iindex = esm2m2seawifs.define_obs_position_from_gridded(seawifs_clim,'chl',frame=0)
out = esm2m2seawifs.interpolate_model_onto_obs_space(lon_obs,lat_obs,esm2m_data,'chl',level=0,frame=0,spval=1.0e+15)
out_2d = esm2m2seawifs.reshape_interpolated_data(jindex,iindex,out)

#print out.min() , out.max()
#print out_2d.min() , out_2d.max()

#plt.figure()
#plt.plot(out)
#plt.plot(lon_obs)
#plt.show()


plt.figure()
#plt.plot(lon_obs,lat_obs,'ko')
plt.pcolor(esm2m2seawifs.lon_gridded_2d,esm2m2seawifs.lat_gridded_2d,out_2d); plt.colorbar()
#plt.clim([8.,18.])
plt.show()
