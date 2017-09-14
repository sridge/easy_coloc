import easy_coloc
import matplotlib.pylab as plt
import numpy as np
import seaborn as sns

roms_grid      = '/Volumes/P1/ROMS-Inputs/CCS1/grid/CCS_7k_0-360_fred_grd.nc'
roms_datadir   = '/Volumes/P7/ROMS/CCS1/CCS1-RD.NVOcobalt23R/monthly/'
O2NOAA         = '../data/O2_bottom_trawl_NOAA_cleaned.csv'

roms_fileavg   = 'CCS1-RD.NVOcobalt23R_avg_YYYY-MM_monthly.nc'
outputdir      = '/Volumes/P4/workdir/raphael/analysis_CCS1-Cobalt/results_EZcoloc/run23R_onto_noaa_oxygen/'
outputdir_noaa = '/Volumes/P4/workdir/raphael/analysis_CCS1-Cobalt/results_EZcoloc/noaa_oxygen/'

firstyear = 1996
lastyear  = 2006
nyears=lastyear-firstyear+1
# create easy_coloc object
EZC     = easy_coloc.easy_coloc(roms_grid,from_global=False,coord_names=['lon_rho','lat_rho'],mask_var='mask_rho')

# read lon/lat of observations as well as depth and o2
# no loop because number of obs is different, obs avail from may to oct

lon_obs_may,  lat_obs_may,  o2_obs_may  = EZC.read_obs_data_from_text(O2NOAA,3,2,4,offset_line=1,separator=',',if_found=',5,')
lon_obs_june, lat_obs_june, o2_obs_june = EZC.read_obs_data_from_text(O2NOAA,3,2,4,offset_line=1,separator=',',if_found=',6,')
lon_obs_july, lat_obs_july, o2_obs_july = EZC.read_obs_data_from_text(O2NOAA,3,2,4,offset_line=1,separator=',',if_found=',7,')
lon_obs_aug,  lat_obs_aug,  o2_obs_aug  = EZC.read_obs_data_from_text(O2NOAA,3,2,4,offset_line=1,separator=',',if_found=',8,')
lon_obs_sept, lat_obs_sept, o2_obs_sept = EZC.read_obs_data_from_text(O2NOAA,3,2,4,offset_line=1,separator=',',if_found=',9,')
lon_obs_oct,  lat_obs_oct,  o2_obs_oct  = EZC.read_obs_data_from_text(O2NOAA,3,2,4,offset_line=1,separator=',',if_found=',10,')

lon_obs_may,  lat_obs_may,  depth_obs_may  = EZC.read_obs_data_from_text(O2NOAA,3,2,1,offset_line=1,separator=',',if_found=',5,')
lon_obs_june, lat_obs_june, depth_obs_june = EZC.read_obs_data_from_text(O2NOAA,3,2,1,offset_line=1,separator=',',if_found=',6,')
lon_obs_july, lat_obs_july, depth_obs_july = EZC.read_obs_data_from_text(O2NOAA,3,2,1,offset_line=1,separator=',',if_found=',7,')
lon_obs_aug,  lat_obs_aug,  depth_obs_aug  = EZC.read_obs_data_from_text(O2NOAA,3,2,1,offset_line=1,separator=',',if_found=',8,')
lon_obs_sept, lat_obs_sept, depth_obs_sept = EZC.read_obs_data_from_text(O2NOAA,3,2,1,offset_line=1,separator=',',if_found=',9,')
lon_obs_oct,  lat_obs_oct,  depth_obs_oct  = EZC.read_obs_data_from_text(O2NOAA,3,2,1,offset_line=1,separator=',',if_found=',10,')

o2_model_may  = np.zeros((len(o2_obs_may),nyears))
o2_model_june = np.zeros((len(o2_obs_june),nyears))
o2_model_july = np.zeros((len(o2_obs_july),nyears))
o2_model_aug  = np.zeros((len(o2_obs_aug),nyears))
o2_model_sept = np.zeros((len(o2_obs_sept),nyears))
o2_model_oct  = np.zeros((len(o2_obs_oct),nyears))

depth_model_may  = np.zeros((len(depth_obs_may),nyears))
depth_model_june = np.zeros((len(depth_obs_june),nyears))
depth_model_july = np.zeros((len(depth_obs_july),nyears))
depth_model_aug  = np.zeros((len(depth_obs_aug),nyears))
depth_model_sept = np.zeros((len(depth_obs_sept),nyears))
depth_model_oct  = np.zeros((len(depth_obs_oct),nyears))

ct=0
for year in np.arange(firstyear,lastyear+1):
	# define filename
	roms_data = roms_datadir+roms_fileavg.replace('YYYY',str(year).zfill(4))
	# project model data onto observation space
	o2_model_may[:,ct]  = EZC.interpolate_model_onto_obs_space(lon_obs_may,lat_obs_may,  roms_data.replace('MM','05'),'o2',level=0,frame=0,spval=1.0e+15)
	o2_model_june[:,ct] = EZC.interpolate_model_onto_obs_space(lon_obs_june,lat_obs_june,roms_data.replace('MM','06'),'o2',level=0,frame=0,spval=1.0e+15)
	o2_model_july[:,ct] = EZC.interpolate_model_onto_obs_space(lon_obs_july,lat_obs_july,roms_data.replace('MM','07'),'o2',level=0,frame=0,spval=1.0e+15)
	o2_model_aug[:,ct]  = EZC.interpolate_model_onto_obs_space(lon_obs_aug,lat_obs_aug,  roms_data.replace('MM','08'),'o2',level=0,frame=0,spval=1.0e+15)
	o2_model_sept[:,ct] = EZC.interpolate_model_onto_obs_space(lon_obs_sept,lat_obs_sept,roms_data.replace('MM','09'),'o2',level=0,frame=0,spval=1.0e+15)
	o2_model_oct[:,ct]  = EZC.interpolate_model_onto_obs_space(lon_obs_oct,lat_obs_oct,  roms_data.replace('MM','10'),'o2',level=0,frame=0,spval=1.0e+15)

	depth_model_may[:,ct]  = EZC.interpolate_model_onto_obs_space(lon_obs_may,lat_obs_may,  roms_grid,'h',spval=1.0e+15)
	depth_model_june[:,ct] = EZC.interpolate_model_onto_obs_space(lon_obs_june,lat_obs_june,roms_grid,'h',spval=1.0e+15)
	depth_model_july[:,ct] = EZC.interpolate_model_onto_obs_space(lon_obs_july,lat_obs_july,roms_grid,'h',spval=1.0e+15)
	depth_model_aug[:,ct]  = EZC.interpolate_model_onto_obs_space(lon_obs_aug,lat_obs_aug,  roms_grid,'h',spval=1.0e+15)
	depth_model_sept[:,ct] = EZC.interpolate_model_onto_obs_space(lon_obs_sept,lat_obs_sept,roms_grid,'h',spval=1.0e+15)
	depth_model_oct[:,ct]  = EZC.interpolate_model_onto_obs_space(lon_obs_oct,lat_obs_oct,  roms_grid,'h',spval=1.0e+15)

	ct=ct+1

# convert units for O2
o2_model_may  = o2_model_may  * 1035 * 22391.6 / 1000.0 # convert to mL/L
o2_model_june = o2_model_june * 1035 * 22391.6 / 1000.0 # convert to mL/L
o2_model_july = o2_model_july * 1035 * 22391.6 / 1000.0 # convert to mL/L
o2_model_aug  = o2_model_aug  * 1035 * 22391.6 / 1000.0 # convert to mL/L
o2_model_sept = o2_model_sept * 1035 * 22391.6 / 1000.0 # convert to mL/L
o2_model_oct  = o2_model_oct  * 1035 * 22391.6 / 1000.0 # convert to mL/L

# write model data projected onto obs space into text file
ct=0
for year in np.arange(firstyear,lastyear+1):
	EZC.write_to_file_two_dataset(outputdir + 'roms_run23R_onto_o2noaa_may_'  + str(year) + '.txt',lon_obs_may, lat_obs_may, depth_model_may[:,ct], o2_model_may[:,ct])
	EZC.write_to_file_two_dataset(outputdir + 'roms_run23R_onto_o2noaa_june_' + str(year) + '.txt',lon_obs_june,lat_obs_june,depth_model_june[:,ct],o2_model_june[:,ct])
	EZC.write_to_file_two_dataset(outputdir + 'roms_run23R_onto_o2noaa_july_' + str(year) + '.txt',lon_obs_july,lat_obs_july,depth_model_july[:,ct],o2_model_july[:,ct])
	EZC.write_to_file_two_dataset(outputdir + 'roms_run23R_onto_o2noaa_aug_'  + str(year) + '.txt',lon_obs_aug, lat_obs_aug, depth_model_aug[:,ct], o2_model_aug[:,ct])
	EZC.write_to_file_two_dataset(outputdir + 'roms_run23R_onto_o2noaa_sept_' + str(year) + '.txt',lon_obs_sept,lat_obs_sept,depth_model_sept[:,ct],o2_model_sept[:,ct])
	EZC.write_to_file_two_dataset(outputdir + 'roms_run23R_onto_o2noaa_oct_'  + str(year) + '.txt',lon_obs_oct, lat_obs_oct, depth_model_oct[:,ct], o2_model_oct[:,ct])
	ct=ct+1

# write data in separate files
EZC.write_to_file_two_dataset(outputdir_noaa + 'oxygen_o2noaa_may'   + '.txt',lon_obs_may, lat_obs_may, depth_obs_may[:], o2_obs_may[:])
EZC.write_to_file_two_dataset(outputdir_noaa + 'oxygen_o2noaa_june'  + '.txt',lon_obs_june,lat_obs_june,depth_obs_june[:],o2_obs_june[:])
EZC.write_to_file_two_dataset(outputdir_noaa + 'oxygen_o2noaa_july'  + '.txt',lon_obs_july,lat_obs_july,depth_obs_july[:],o2_obs_july[:])
EZC.write_to_file_two_dataset(outputdir_noaa + 'oxygen_o2noaa_aug'   + '.txt',lon_obs_aug, lat_obs_aug, depth_obs_aug[:], o2_obs_aug[:])
EZC.write_to_file_two_dataset(outputdir_noaa + 'oxygen_o2noaa_sept'  + '.txt',lon_obs_sept,lat_obs_sept,depth_obs_sept[:],o2_obs_sept[:])
EZC.write_to_file_two_dataset(outputdir_noaa + 'oxygen_o2noaa_oct'   + '.txt',lon_obs_oct, lat_obs_oct, depth_obs_oct[:], o2_obs_oct[:])

