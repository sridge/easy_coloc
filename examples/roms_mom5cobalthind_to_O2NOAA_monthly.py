import easy_coloc
import matplotlib.pylab as plt
import numpy as np
import seaborn as sns

# here we use the clim files (uncorrected with WOA13) that are interpolated from the cobalt hindcast here :
# /Volumes/P1/Data/GFDL/Cobalt_clim

roms_grid      = '/Volumes/P1/ROMS-Inputs/CCS1/grid/CCS_7k_0-360_fred_grd.nc'
mom5_datadir   = '/Volumes/P4/workdir/raphael/workspace-raphael.git/preprocessing-roms/ccs1-cobalt-hindcast/Clim_bio/uncorrected/'
O2NOAA         = '../data/O2_bottom_trawl_NOAA_cleaned.csv'

mom5_fileavg   = 'CCS1_clim_bio_GFDL_mMM.nc'
outputdir      = '/Volumes/P4/workdir/raphael/analysis_CCS1-Cobalt/results_EZcoloc/run_cobalt_mom5_onto_noaa_oxygen/'

nyears=1
# create easy_coloc object
EZC     = easy_coloc.easy_coloc(roms_grid,from_global=False,coord_names=['lon_rho','lat_rho'],mask_var='mask_rho')

# read lon/lat of observations as well as depth and o2
# no loop because number of obs is different, obs avail from may to oct

lon_obs_may,  lat_obs_may   = EZC.define_obs_position_from_text(O2NOAA,3,2,offset_line=1,separator=',',if_found=',5,')
lon_obs_june, lat_obs_june  = EZC.define_obs_position_from_text(O2NOAA,3,2,offset_line=1,separator=',',if_found=',6,')
lon_obs_july, lat_obs_july  = EZC.define_obs_position_from_text(O2NOAA,3,2,offset_line=1,separator=',',if_found=',7,')
lon_obs_aug,  lat_obs_aug   = EZC.define_obs_position_from_text(O2NOAA,3,2,offset_line=1,separator=',',if_found=',8,')
lon_obs_sept, lat_obs_sept  = EZC.define_obs_position_from_text(O2NOAA,3,2,offset_line=1,separator=',',if_found=',9,')
lon_obs_oct,  lat_obs_oct   = EZC.define_obs_position_from_text(O2NOAA,3,2,offset_line=1,separator=',',if_found=',10,')

# define filename
mom5_data = mom5_datadir+mom5_fileavg
# project model data onto observation space
o2_model_may  = EZC.interpolate_model_onto_obs_space(lon_obs_may,lat_obs_may,  mom5_data.replace('MM','05'),'o2',level=0,frame=0,spval=1.0e+15)
o2_model_june = EZC.interpolate_model_onto_obs_space(lon_obs_june,lat_obs_june,mom5_data.replace('MM','06'),'o2',level=0,frame=0,spval=1.0e+15)
o2_model_july = EZC.interpolate_model_onto_obs_space(lon_obs_july,lat_obs_july,mom5_data.replace('MM','07'),'o2',level=0,frame=0,spval=1.0e+15)
o2_model_aug  = EZC.interpolate_model_onto_obs_space(lon_obs_aug,lat_obs_aug,  mom5_data.replace('MM','08'),'o2',level=0,frame=0,spval=1.0e+15)
o2_model_sept = EZC.interpolate_model_onto_obs_space(lon_obs_sept,lat_obs_sept,mom5_data.replace('MM','09'),'o2',level=0,frame=0,spval=1.0e+15)
o2_model_oct  = EZC.interpolate_model_onto_obs_space(lon_obs_oct,lat_obs_oct,  mom5_data.replace('MM','10'),'o2',level=0,frame=0,spval=1.0e+15)

depth_model_may  = EZC.interpolate_model_onto_obs_space(lon_obs_may,lat_obs_may,  roms_grid,'h',spval=1.0e+15)
depth_model_june = EZC.interpolate_model_onto_obs_space(lon_obs_june,lat_obs_june,roms_grid,'h',spval=1.0e+15)
depth_model_july = EZC.interpolate_model_onto_obs_space(lon_obs_july,lat_obs_july,roms_grid,'h',spval=1.0e+15)
depth_model_aug  = EZC.interpolate_model_onto_obs_space(lon_obs_aug,lat_obs_aug,  roms_grid,'h',spval=1.0e+15)
depth_model_sept = EZC.interpolate_model_onto_obs_space(lon_obs_sept,lat_obs_sept,roms_grid,'h',spval=1.0e+15)
depth_model_oct  = EZC.interpolate_model_onto_obs_space(lon_obs_oct,lat_obs_oct,  roms_grid,'h',spval=1.0e+15)

# convert units for O2
o2_model_may  = o2_model_may  * 1035 * 22391.6 / 1000.0 # convert to mL/L
o2_model_june = o2_model_june * 1035 * 22391.6 / 1000.0 # convert to mL/L
o2_model_july = o2_model_july * 1035 * 22391.6 / 1000.0 # convert to mL/L
o2_model_aug  = o2_model_aug  * 1035 * 22391.6 / 1000.0 # convert to mL/L
o2_model_sept = o2_model_sept * 1035 * 22391.6 / 1000.0 # convert to mL/L
o2_model_oct  = o2_model_oct  * 1035 * 22391.6 / 1000.0 # convert to mL/L

# write model data projected onto obs space into text file
EZC.write_to_file_two_dataset(outputdir + 'roms_mom5_onto_o2noaa_may'  + '.txt',lon_obs_may, lat_obs_may, depth_model_may, o2_model_may)
EZC.write_to_file_two_dataset(outputdir + 'roms_mom5_onto_o2noaa_june' + '.txt',lon_obs_june,lat_obs_june,depth_model_june,o2_model_june)
EZC.write_to_file_two_dataset(outputdir + 'roms_mom5_onto_o2noaa_july' + '.txt',lon_obs_july,lat_obs_july,depth_model_july,o2_model_july)
EZC.write_to_file_two_dataset(outputdir + 'roms_mom5_onto_o2noaa_aug'  + '.txt',lon_obs_aug, lat_obs_aug, depth_model_aug, o2_model_aug)
EZC.write_to_file_two_dataset(outputdir + 'roms_mom5_onto_o2noaa_sept' + '.txt',lon_obs_sept,lat_obs_sept,depth_model_sept,o2_model_sept)
EZC.write_to_file_two_dataset(outputdir + 'roms_mom5_onto_o2noaa_oct'  + '.txt',lon_obs_oct, lat_obs_oct, depth_model_oct, o2_model_oct)

