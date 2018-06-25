Command Line Provenance
=======================


Introduction
------------

``cmdline_provenance`` is a Python package for keeping track of your data processing steps.

It was inspired by the popular `NCO <http://nco.sourceforge.net/>`_ and
`CDO <https://code.mpimet.mpg.de/projects/cdo>`_ command line tools,
which automatically generate a record of what was executed at the command line,
append that record to the history attribute from the input (netCDF) data file,
and then set the new extended record as the history attribute of the output (netCDF) data file.

For example, after selecting the 2001-2005 time period from a rainfall data file
and then deleting the ``long_name`` file attribute,
the command log would look as follows:

.. code-block:: bash

   Fri Dec 08 10:05:47 2017: ncatted -O -a long_name,pr,d,, rainfall_data_200101-200512.nc
   Fri Dec 01 07:59:16 2017: cdo seldate,2001-01-01,2005-12-31 rainfall_data_185001-200512.nc rainfall_data_200101-200512.nc

Following this simple approach to data provenance,
it is possible maintain a record of all data processing steps
from intial download/creation of your data files to the end result (e.g. a .png image).

``cmdline_provenance`` contains a series of functions for generating history records in the NCO/CDO format,
and for combining the current record with previous records to maintain a complete command log.


Installation
------------

.. code-block:: bash

   $ pip install cmdline-provenance


Usage
-----

netCDF output
^^^^^^^^^^^^^^^^^

Let's say you have a script ``calc_density.py``,
which takes two netCDF files as input (an ocean temperature and ocean salinity file)
and outputs a single ocean density netCDF file.
It can be run at the command line as follows:

.. code-block:: bash
  
   $ python calc_density.py temperature_data.nc salinity_data.nc density_data.nc
   

If the history attribute within the input files is unimportant,
a stand-alone record of that command line entry can be created 
within the ``calc_density.py`` script, as follows:

.. code-block:: python

   import cmdline_provenance as cmdprov
   
   record = cmdprov.new_cmdline_history()
   
That record would read something like:
   
   
non-netCDF output
^^^^^^^^^^^^^^^^^^^^^

Blah

