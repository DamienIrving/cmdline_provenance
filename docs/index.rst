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

creating a log
^^^^^^^^^^^^^^

Let's say we have a script ``ocean_analysis.py``,
which takes two files as input (an ocean temperature and ocean salinity file)
and outputs a single file.
These input files could be CSV (.csv) or netCDF (.nc) or some other format,
and the output could be another data file (e.g. .csv or .nc) or a figure (e.g. .png, .eps).
For the sake of example, we will simply use an unspecified format (.fmt) for now.

The script can be run at the command line as follows:

.. code-block:: bash
  
   $ python ocean_analysis.py temperature_data.fmt salinity_data.fmt output.fmt
   

To create a new log that captures this command line entry,
we can use the ``new_log`` function:

.. code-block:: python

   >>> import cmdline_provenance as cmdprov
   >>> my_log = cmdprov.new_log()
   >>> print(my_log)
   Tue Jun 26 11:24:46 2018: /Applications/anaconda/bin/python ocean_analysis.py temperature_data.fmt salinity_data.fmt output.fmt
   
If our script is tracked in a version controlled git repository,
we can provide the location of that repository (the top-level directory)
and the log entry will specify the precise version of ``ocean_analysis.py`` that was executed:

.. code-block:: python

   >>> my_log = cmdprov.new_log(git_repo='/path/to/git/repo/')
   >>> print(my_log)
   Tue Jun 26 11:24:46 2018: /Applications/anaconda/bin/python ocean_analysis.py temperature_data.fmt salinity_data.fmt output.fmt (Git hash: 026301f)


Each commit in a git repository is associated with a unique 40-character identifier known as a hash.
The ``new_log`` function has included the first 7-characters
of the hash associated with the latest commit to the repository,
which is sufficient information to revert back to that previous version of ``ocean_analysis.py``.


outputting a log
^^^^^^^^^^^^^^^^

If our output file is a self-describing file format (i.e. a format that carries its metadata with it),
then we would include our new log in the file metadata.
For instance, a common convention in weather and climate science is to include the command log
in the global history attribute of netCDF data files.
If we were using the iris library (for instance)
to read and write netCDF files using its cube data structure,
the process would look something like this:

.. code-block:: python

   >>> import iris
   >>> import cmdline_provenance as cmdprov
   >>> my_log = cmdprov.new_log(git_repo='/path/to/git/repo/')
   ...
   >>> type(output_cube)
   iris.cube.Cube
   >>> output_cube.attributes['history'] = my_log
   >>> iris.save(output_cube, 'output.nc')

If the output file was not a self-describing format (e.g. a .png image),
then we can write a separate log file (i.e. a simple text file with the log in it)
using the ``write_log`` function.

.. code-block:: python

   >>> outfile = 'output.png'
   >>> logfile = 'output.log'
   >>> cmdprov.write_log(logfile, my_log)


While it's not a formal requirement of the ``write_log`` function,
it's good practice to make the name of the log file exactly the same as the name of the output file,
just with a different file extension such as .log or .txt.

input file history
^^^^^^^^^^^^^^^^^^

If we want a complete log...
