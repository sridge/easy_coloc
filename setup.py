import os
from numpy.distutils.core import setup, Extension

#fill_msg_grid    = Extension(name = 'brushcutter.fill_msg_grid',
#                             sources = ['brushcutter/f90/fill_msg_grid.f90'])

setup(
    name = "easy_coloc",
    version = "1.0",
    author = "Raphael Dussin",
    author_email = "raphael.dussin@gmail.com",
    description = ("A package for project model onto obs space " ),
    license = "GPLv3",
    keywords = "ocean modeling / observations",
    url = "",
    packages=['easy_coloc'] #,
#    ext_modules = [fill_msg_grid]
)


