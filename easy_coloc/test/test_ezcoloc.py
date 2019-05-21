# requires pytest-datafiles
import os
from easy_coloc import lib_easy_coloc
import xarray as xr
import pandas as pd

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'test_files/',
    )


def test_ar07w(datafiles):
    ar07w = pd.read_csv(FIXTURE_DIR + 'AR07W_stations.txt',
                        skipinitialspace=True)
    ds = xr.open_dataset(FIXTURE_DIR + 'woa_labrador.nc', decode_times=False)
    proj = lib_easy_coloc.projection(ar07w['lon'].values,
                                     ar07w['lat'].values,
                                     grid=ds)
    fld = proj.run(ds['t_an'][:])
    assert fld.shape == (1, 102, 30)
    return None
