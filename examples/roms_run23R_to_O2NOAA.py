import easy_coloc
import matplotlib.pylab as plt
import numpy as np

roms_grid      = '/Volumes/P9/ROMS-Inputs/CCS1/grid/CCS_7k_0-360_fred_grd.nc'
roms_data_june = '/Volumes/P7/ROMS/CCS1/CCS1-RD.NVOcobalt23R/interannual_monthly/CCS1-RD.NVOcobalt23R_avg_1996-2006-06_monthly.nc'
roms_data_july = '/Volumes/P7/ROMS/CCS1/CCS1-RD.NVOcobalt23R/interannual_monthly/CCS1-RD.NVOcobalt23R_avg_1996-2006-07_monthly.nc'
roms_data_aug  = '/Volumes/P7/ROMS/CCS1/CCS1-RD.NVOcobalt23R/interannual_monthly/CCS1-RD.NVOcobalt23R_avg_1996-2006-08_monthly.nc'
O2NOAA         = '../data/O2_bottom_trawl_NOAA_cleaned.csv'
outputdir      = '/Volumes/P4/workdir/raphael/analysis_CCS1-Cobalt/results_EZcoloc/run23R_onto_noaa_oxygen/'

# create easy_coloc object
EZC     = easy_coloc.easy_coloc(roms_grid,from_global=False,coord_names=['lon_rho','lat_rho'],mask_var='mask_rho')

# define list of obs positions from text file for june to august
lon_obs_june, lat_obs_june, o2_obs_june = EZC.read_obs_data_from_text(O2NOAA,3,2,4,offset_line=1,separator=',',if_found=',6,')
lon_obs_july, lat_obs_july, o2_obs_july = EZC.read_obs_data_from_text(O2NOAA,3,2,4,offset_line=1,separator=',',if_found=',7,')
lon_obs_aug,  lat_obs_aug,  o2_obs_aug  = EZC.read_obs_data_from_text(O2NOAA,3,2,4,offset_line=1,separator=',',if_found=',8,')

lon_obs_june, lat_obs_june, depth_obs_june = EZC.read_obs_data_from_text(O2NOAA,3,2,1,offset_line=1,separator=',',if_found=',6,')
lon_obs_july, lat_obs_july, depth_obs_july = EZC.read_obs_data_from_text(O2NOAA,3,2,1,offset_line=1,separator=',',if_found=',7,')
lon_obs_aug,  lat_obs_aug,  depth_obs_aug  = EZC.read_obs_data_from_text(O2NOAA,3,2,1,offset_line=1,separator=',',if_found=',8,')

# project model data onto observation space
o2_model_june = EZC.interpolate_model_onto_obs_space(lon_obs_june,lat_obs_june,roms_data_june,'o2',level=0, frame=0,spval=1.0e+15)
o2_model_july = EZC.interpolate_model_onto_obs_space(lon_obs_july,lat_obs_july,roms_data_july,'o2',level=0, frame=0,spval=1.0e+15)
o2_model_aug  = EZC.interpolate_model_onto_obs_space(lon_obs_aug, lat_obs_aug, roms_data_aug, 'o2',level=0, frame=0,spval=1.0e+15)

depth_model_june = EZC.interpolate_model_onto_obs_space(lon_obs_june,lat_obs_june,roms_grid,'h',spval=1.0e+15)
depth_model_july = EZC.interpolate_model_onto_obs_space(lon_obs_july,lat_obs_july,roms_grid,'h',spval=1.0e+15)
depth_model_aug  = EZC.interpolate_model_onto_obs_space(lon_obs_aug, lat_obs_aug, roms_grid,'h',spval=1.0e+15)

o2_model_june = o2_model_june * 1035 * 22391.6 / 1000.0 # convert to mL/L
o2_model_july = o2_model_july * 1035 * 22391.6 / 1000.0 # convert to mL/L
o2_model_aug  = o2_model_aug  * 1035 * 22391.6 / 1000.0 # convert to mL/L

# write model data projected onto obs space into text file
EZC.write_to_file_two_dataset(outputdir + 'roms_run23R_onto_o2noaa_june_1996-2006'  + '.txt',lon_obs_june, lat_obs_june, depth_model_june, o2_model_june)
EZC.write_to_file_two_dataset(outputdir + 'roms_run23R_onto_o2noaa_july_1996-2006'  + '.txt',lon_obs_july, lat_obs_july, depth_model_july, o2_model_july)
EZC.write_to_file_two_dataset(outputdir + 'roms_run23R_onto_o2noaa_aug_1996-2006'   + '.txt',lon_obs_aug,  lat_obs_aug,  depth_model_aug,  o2_model_aug)
