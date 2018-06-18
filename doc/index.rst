.. easy_coloc documentation master file, created by
   sphinx-quickstart on Mon Jun 18 17:08:17 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to easy_coloc's documentation!
======================================

**easy_coloc** uses the ESMF_ library to interpolate gridded data, such as Ocean
General Circulation Model outputs onto observations. Observation points can
be provided in a csv or gridded netcdf file. Gridded outputs can then be
projected onto the observation space using the ESMF_ locstream procedure.

.. toctree::
   :maxdepth: 1

   install
   examples

.. _ESMF: https://www.earthsystemcog.org/projects/esmf/


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
