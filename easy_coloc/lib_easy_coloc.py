import ESMF as _ESMF
import xarray as _xr
import numpy as _np

class projection():

    def __init__(self, lon_obs, lat_obs, grid=None, lon_grid=None, lat_grid=None,
                 from_global=True, coord_names=['lon','lat'], dim_names=['lon','lat']):
        ''' construct the source grid ESMF from xarray or numpy.array
        lon_obs : numpy array
        lat_obs : numpy array
        grid : xarray dataset
        lon_grid  : numpy array
        lat_grid  : numpy array
        from_global : bool
        coord_names : list
        dim_names : list
        '''

        if grid is not None:
            # get lon and lat from xarray dataset
            #assert type(grid) == 'xarray.core.dataset.Dataset'
            lon_raw = grid[coord_names[0]].values
            lat_raw = grid[coord_names[1]].values

        else:
            #assert type(lon) == numpy.array
            #assert type(lat) == numpy.array
            # lon and lat are passed as numpy array
            # make them 2d arrays, if needed
            lon_raw = lon_grid ; lat_raw = lat_grid

        if len(lon_raw.shape) == 1:
            lon_src, lat_src = _np.meshgrid(lon_raw,lat_raw)
        else:
            lon_src = lon_raw ; lat_src = lat_raw

        ny, nx = lon_src.shape

        # construct the ESMF grid object
        self.model_grid = _ESMF.Grid(_np.array([nx,ny]))
        self.model_grid.add_coords(staggerloc=[_ESMF.StaggerLoc.CENTER])
        self.model_grid.coords[_ESMF.StaggerLoc.CENTER]
        self.model_grid.coords[_ESMF.StaggerLoc.CENTER][0][:]=lon_src.T
        self.model_grid.coords[_ESMF.StaggerLoc.CENTER][1][:]=lat_src.T
        self.model_grid.is_sphere=from_global

        # import obs location into ESMF locstream object
        self.nobs = len(lon_obs)
        self.locstream_obs = _ESMF.LocStream(self.nobs, coord_sys=_ESMF.CoordSys.SPH_DEG)
        self.locstream_obs["ESMF:Lon"] = lon_obs[:]
        self.locstream_obs["ESMF:Lat"] = lat_obs[:]

        return None


    def run(self,data,mask_value=None):
        ''' run the projection
        var : str
        data : numpy.array
        level : int

        '''
        # TO DO: ideally we'd like to use the src_mask_values property
        # of the ESMF Regridder. But that requires creating an object for each level
        # It seems that setting the masked points to np.nan does the work at lower cost

        # create field object for model data
        field_model = _ESMF.Field(self.model_grid, staggerloc=_ESMF.StaggerLoc.CENTER)
        # create field object for observation locations
        field_obs = _ESMF.Field(self.locstream_obs)

        interpolator = _ESMF.Regrid(field_model, field_obs,
                                    regrid_method=_ESMF.RegridMethod.BILINEAR,
                                    unmapped_action=_ESMF.UnmappedAction.IGNORE)#,
                                    #src_mask_values = self.mask_values) # esmf uses mask value, not spval

        if type(data) != 'numpy.array':
            data = data.values

        if len(data.shape) == 4: # T,Z,Y,X
            nframes, nlevels, ny, nx = data.shape
            nlevels=data.shape[1]
        elif len(data.shape) == 3: #Z,Y,X
            nframes=1
            nlevels, ny, nx = data.shape
        elif len(data.shape) == 2: #Y,X
            nframes=1
            nlevels=1
            ny, nx = data.shape
        else:
            print('this will fail')

        data = _np.reshape(data, (nframes, nlevels, ny, nx))

        data_out = _np.empty((nframes, nlevels, self.nobs))

        for kframe in _np.arange(nframes):
            for klevel in _np.arange(nlevels):
                datain = data[kframe,klevel,:,:].transpose()
                if mask_value is not None:
                    datain[_np.where(datain == mask_value)] = _np.nan # ugly, cf above

                field_model.data[:] = datain

                # run the interpolator
                field_obs = interpolator(field_model, field_obs)
                data_model_interp = field_obs.data.copy()

                data_out[kframe,klevel,:] = data_model_interp

        field_model.destroy()
        field_obs.destroy()
        interpolator.destroy()

        return data_out
