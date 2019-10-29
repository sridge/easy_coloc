import ESMF as _ESMF
import numpy as _np
import pandas as pd


def grid_create_from_coordinates_periodic(longitudes, latitudes, lon_corners=False, lat_corners=False,
                                          corners=False, domask=False):
    """
    Create a 2 dimensional periodic Grid using the 'longitudes' and 'latitudes'.
    source: http://www.earthsystemmodeling.org/esmf_releases/public/last/esmpy_doc/html/examples.html#create-a-periodic-grid
    :param longitudes: longitude coordinate values at cell centers
    :param latitudes: latitude coordinate values at cell centers
    :param lon_corners: longitude coordinate values at cell corners
    :param lat_corners: latitude coordinate values at cell corners
    :param corners: boolean to determine whether or not to add corner coordinates to this grid
    :param domask: boolean to determine whether to set an arbitrary mask or not
    :return: grid
    """
    
    [lon, lat] = [0, 1]

    # create a grid given the number of grid cells in each dimension the center stagger location is allocated
    max_index = np.array([len(longitudes), len(latitudes)])
    grid = ESMF.Grid(max_index, num_peri_dims=1, staggerloc=[ESMF.StaggerLoc.CENTER])

    # set the grid coordinates using numpy arrays, parallel case is handled using grid bounds
    gridXCenter = grid.get_coords(lon)
    lon_par = longitudes[grid.lower_bounds[ESMF.StaggerLoc.CENTER][lon]:grid.upper_bounds[ESMF.StaggerLoc.CENTER][lon]]
    gridXCenter[...] = lon_par.reshape((lon_par.size, 1))

    gridYCenter = grid.get_coords(lat)
    lat_par = latitudes[grid.lower_bounds[ESMF.StaggerLoc.CENTER][lat]:grid.upper_bounds[ESMF.StaggerLoc.CENTER][lat]]
    gridYCenter[...] = lat_par.reshape((1, lat_par.size))

    # create grid corners in a slightly different manner to account for the bounds format common in CF-like files
    if corners:
        grid.add_coords([ESMF.StaggerLoc.CORNER])
        lbx = grid.lower_bounds[ESMF.StaggerLoc.CORNER][lon]
        ubx = grid.upper_bounds[ESMF.StaggerLoc.CORNER][lon]
        lby = grid.lower_bounds[ESMF.StaggerLoc.CORNER][lat]
        uby = grid.upper_bounds[ESMF.StaggerLoc.CORNER][lat]

        gridXCorner = grid.get_coords(lon, staggerloc=ESMF.StaggerLoc.CORNER)
        for i0 in range(ubx - lbx - 1):
            gridXCorner[i0, :] = lon_corners[i0+lbx, 0]
        gridXCorner[i0 + 1, :] = lon_corners[i0+lbx, 1]

        gridYCorner = grid.get_coords(lat, staggerloc=ESMF.StaggerLoc.CORNER)
        for i1 in range(uby - lby - 1):
            gridYCorner[:, i1] = lat_corners[i1+lby, 0]
        gridYCorner[:, i1 + 1] = lat_corners[i1+lby, 1]

    # add an arbitrary mask
    if domask:
        mask = grid.add_item(ESMF.GridItem.MASK)
        mask[:] = 1
        mask[np.where((1.75 <= gridXCenter.any() < 2.25) &
                      (1.75 <= gridYCenter.any() < 2.25))] = 0

    return grid

#------------------------------------------------------------------------------
#
#------------------------------------------------------------------------------

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
        self.model_grid = grid_create_from_coordinates_periodic(lon_src,lat_src)

        # import obs location into ESMF locstream object
        self.nobs = len(lon_obs)
        self.locstream_obs = _ESMF.LocStream(self.nobs,
                                             coord_sys=_ESMF.CoordSys.SPH_DEG)
        self.locstream_obs["ESMF:Lon"] = lon_obs[:]
        self.locstream_obs["ESMF:Lat"] = lat_obs[:]

        return None

    def run(self, data, mask_value=None, outtype='ndarray'):
        ''' run the projection
        var : str
        data : numpy.array
        level : int
        outtype : ndarray or dataframe

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

        if type(data) != 'numpy.array':
            data = data.values

        if len(data.shape) == 4:  # T,Z,Y,X
            nframes, nlevels, ny, nx = data.shape
            nlevels = data.shape[1]
        elif len(data.shape) == 3:  # Z,Y,X
            nframes = 1
            nlevels, ny, nx = data.shape
        elif len(data.shape) == 2:  # Y,X
            nframes = 1
            nlevels = 1
            ny, nx = data.shape
        else:
            print('this will fail')

        data = _np.reshape(data, (nframes, nlevels, ny, nx))

        data_out = _np.empty((nframes, nlevels, self.nobs))

        df_out = pd.DataFrame()

        for kframe in _np.arange(nframes):
            for klevel in _np.arange(nlevels):
                datain = data[kframe, klevel, :, :].transpose()
                if mask_value is not None:
                    # ugly fix, cf note above
                    datain[_np.where(datain == mask_value)] = _np.nan

                field_model.data[:] = datain

                # run the interpolator
                field_obs = interpol(field_model, field_obs)
                data_model_interp = field_obs.data.copy()

                data_out[kframe, klevel, :] = data_model_interp

                tmp = {'lon_stations': self.lon_obs,
                       'lat_stations': self.lat_obs,
                       'data_stations': data_out[kframe, klevel, :]}

                df = pd.DataFrame(tmp)
                df_out = pd.concat([df_out, df])

        field_model.destroy()
        field_obs.destroy()
        interpol.destroy()

        if outtype == 'ndarray':
            return data_out
        elif outtype == 'dataframe':
            return df_out
