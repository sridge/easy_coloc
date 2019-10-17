import ESMF as _ESMF
import numpy as _np
import pandas as pd
import uuid as _uuid
import dask.array as _dsa

import xarray as _xr

class projection():

    def __init__(self, lon_obs, lat_obs, grid=None,
                 lon_grid=None, lat_grid=None,
                 from_global=True, coord_names=['lon', 'lat'],
                 dim_names=['lon', 'lat']):
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

        self.lon_obs = lon_obs
        self.lat_obs = lat_obs

        if grid is not None:
            # get lon and lat from xarray dataset
            # assert type(grid) == 'xarray.core.dataset.Dataset'
            lon_raw = grid[coord_names[0]].values
            lat_raw = grid[coord_names[1]].values

        else:
            # assert type(lon) == numpy.array
            # assert type(lat) == numpy.array
            # lon and lat are passed as numpy array
            # make them 2d arrays, if needed
            lon_raw = lon_grid
            lat_raw = lat_grid

        if len(lon_raw.shape) == 1:
            lon_src, lat_src = _np.meshgrid(lon_raw, lat_raw)
        else:
            lon_src = lon_raw
            lat_src = lat_raw

        ny, nx = lon_src.shape

        # construct the ESMF grid object
        self.model_grid = _ESMF.Grid(_np.array([nx, ny]))
        self.model_grid.add_coords(staggerloc=[_ESMF.StaggerLoc.CENTER])
        self.model_grid.coords[_ESMF.StaggerLoc.CENTER]
        self.model_grid.coords[_ESMF.StaggerLoc.CENTER][0][:] = lon_src.T
        self.model_grid.coords[_ESMF.StaggerLoc.CENTER][1][:] = lat_src.T
        self.model_grid.is_sphere = from_global

        # import obs location into ESMF locstream object
        self.nobs = len(lon_obs)
        self.locstream_obs = _ESMF.LocStream(self.nobs,
                                             coord_sys=_ESMF.CoordSys.SPH_DEG)
        self.locstream_obs["ESMF:Lon"] = lon_obs[:]
        self.locstream_obs["ESMF:Lat"] = lat_obs[:]

        return None

    def run(self, data, mask_value=None, outtype='ndarray',
            xdim='lon', ydim='lat', zdim='depth', timedim='time',
            memberdim='member'):

        ''' run the projection
        var : str
        data : xarray.DataArray
        level : int
        outtype : xarray.DataArray

        '''
        # TO DO: ideally we'd like to use the src_mask_values property
        # of the ESMF Regridder. But that requires creating an object
        # for each level
        # It seems that setting the masked points to np.nan does the
        # work at lower cost

        # create field object for model data
        field_model = _ESMF.Field(self.model_grid,
                                  staggerloc=_ESMF.StaggerLoc.CENTER)
        # create field object for observation locations
        field_obs = _ESMF.Field(self.locstream_obs)

        interpol = _ESMF.Regrid(field_model, field_obs,
                                regrid_method=_ESMF.RegridMethod.BILINEAR,
                                unmapped_action=_ESMF.UnmappedAction.IGNORE)

        # check for input data shape
        if timedim not in data.dims:
            data = data.expand_dims(dim=timedim)
        if memberdim not in data.dims:
            data = data.expand_dims(dim=memberdim)

        chunks = (1, 1, 1, self.nobs)
        nmem = len(data[memberdim])
        nrec = len(data[timedim])
        nlev = len(data[zdim])
        shape = (nmem, nrec, nlev, self.nobs)

        def compute_chunk(lev, rec, mem):
            data2d = data.isel({memberdim: mem, timedim: rec, zdim: lev}).values
            #print(data2d)
            return self.interp_chunk(data2d, interpol, mask_value)[None, None]

# this should work but crashes weirdly
#        dsk = {(data.name, mem, rec, lev, 0): (compute_chunk, lev, rec, mem)
#            for lev in range(nlev)
#            for rec in range(nrec)
#            for mem in range(nmem)}
#
#        out = _dsa.Array(dsk, data.name, chunks,
#                         dtype=_np.dtype('float'), shape=shape)

        # try a dirty loop
        npout = _np.empty(shape)
        for mem in range(nmem):
            for rec in range(nrec):
                for lev in range(nlev):
                    npout[mem, rec, lev,:] = compute_chunk(lev, rec, mem)

        field_model.destroy()
        field_obs.destroy()
        interpol.destroy()

        # need to add coords
        #xout = _xr.DataArray(data=out, dims=(memberdim, timedim, zdim, 'station'))
        xout = _xr.DataArray(data=npout, dims=(memberdim, timedim, zdim, 'station'))
        if outtype == 'ndarray':
            return xout.values
        elif outtype == 'xarray':
            return xout

    def interp_chunk(self, data2d, interpol, mask_value):
 
        # create field object for model data
        field_model_local = _ESMF.Field(self.model_grid,
                                        staggerloc=_ESMF.StaggerLoc.CENTER)
        # create field object for observation locations
        field_obs_local = _ESMF.Field(self.locstream_obs)
        # this is the eager part
        data2d = data2d.transpose() # needed for ESMPy, could be done more elegantly
        if mask_value is not None:
            # ugly fix, cf note above
            data2d[_np.where(data2d == mask_value)] = _np.nan
        # feed it to ESMPy structure
        field_model_local.data[:] = data2d
        # run the interpolator
        field_obs_local = interpol(field_model_local, field_obs_local)
        data_model_interp = field_obs_local.data.copy()
        field_model_local.destroy()
        field_obs_local.destroy()
        return data_model_interp
