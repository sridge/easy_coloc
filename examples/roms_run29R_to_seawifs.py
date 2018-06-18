import easy_coloc
import matplotlib.pylab as plt
import subprocess as sp
import numpy as np
import datetime as dt

def get_output(cmd):
	''' cmd is the string we want to execute in the shell
	and have the output'''
	out = sp.check_output(cmd,shell=True).replace('\n',' ').split()
	return out

roms_grid = '/Volumes/P1/ROMS-Inputs/CCS1/grid/CCS_7k_0-360_fred_grd.nc'
roms_data_root = '/Volumes/P7/ROMS/CCS1/CCS1-RD.NVOcobalt29R/'
seawifs_clim = '../data/seawifs_ccs_grd.nc'
dirout = '/Volumes/P4/workdir/raphael/work_ezcoloc_seawifs/'
fyear=1996
lyear=2006

# create an easy_coloc object, basically defining model grid
roms2seawifs = easy_coloc.easy_coloc(roms_grid,from_global=False,coord_names=['lon_rho','lat_rho'],mask_var='mask_rho')
# from seawifs netcdf file, we extract the position of the valid observation (non-masked or non-missing value)
# create a list of positions in geographical and obs grid space
lon_obs, lat_obs = roms2seawifs.define_obs_position_from_gridded_simple(seawifs_clim)

for year in np.arange(fyear,lyear+1):
	cyear=str(year)
	listfiles = get_output(' ls ' + roms_data_root + cyear + ' | grep dia ' )
	for tfile in listfiles:
		print('working on file ', tfile)
		datestring = tfile.replace('_',' ').split()[2].replace('.nc','')
		date = dt.datetime.strptime(datestring,'%Y-%m-%dT%H:%M:%S')
		roms_data = roms_data_root + cyear + '/' + tfile
		output_txt = dirout + 'chl_on_seawifs_grd_' + tfile.replace('.nc','.txt')
		# for every file, project model data onto observation space
		data_model = roms2seawifs.interpolate_model_onto_obs_space(lon_obs,lat_obs,roms_data,'chl',level=-1,frame=0,spval=1.0e+15)
		# write model data into text file that can be read by pandas
		roms2seawifs.write_to_file_with_date(output_txt,lon_obs,lat_obs,data_model,date,writespval=False,spval=1.0e+15)

