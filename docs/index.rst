Command Line Provenance
=======================

.. toctree::
   :maxdepth: 3
   :hidden:
   
   api_reference
   

Introduction
------------

``cmdline_provenance`` is a Python package for keeping track of your data processing steps.

It was inspired by the popular `NCO <http://nco.sourceforge.net/>`_ and
`CDO <https://code.mpimet.mpg.de/projects/cdo>`_ command line tools,
which are used to manipulate the data and/or metadata contained in netCDF files
(a self-describing file format that is popular in the weather and climate sciences). 
These tools generate a record of what was executed at the command line,
append that record to the history attribute from the input data file,
and then set this command log as the history attribute of the output data file.

For example, after using NCO and CDO to
select the 2001-2005 time period from a rainfall data file
and then delete the ``long_name`` file attribute,
the command log would look as follows:

.. code-block:: bash

   Fri Dec 08 10:05:47 2017: ncatted -O -a long_name,pr,d,, rainfall_data_2001-2005.nc
   Fri Dec 01 07:59:16 2017: cdo seldate,2001-01-01,2005-12-31 rainfall_data_1850-2005.nc rainfall_data_2001-2005.nc

Following this simple approach to data provenance,
it is possible maintain a record of all data processing steps
from intial download/creation of the data files to the end result (e.g. a .png image).

``cmdline_provenance`` contains a function for generating command logs in the NCO/CDO format,
in addition to simple functions for reading and writing log files.


Installation
------------

.. code-block:: bash

   $ pip install cmdline-provenance

or

.. code-block:: bash

   $ conda install cmdline_provenance

Usage
-----

creating a log
^^^^^^^^^^^^^^

Let's say we have a script ``ocean_analysis.py``,
which takes two files as input (an ocean temperature and ocean salinity file)
and outputs a single file.
These input files could be CSV (.csv) or netCDF (.nc) or some other format,
and the output could be another data file (e.g. .csv or .nc) or an image (e.g. .png, .eps).
For the sake of example, we will simply use an unspecified format (.fmt) for now.

The script can be run at the command line as follows:

.. code-block:: bash
  
   $ python ocean_analysis.py temperature_data.fmt salinity_data.fmt output.fmt
   
To create a new log that captures this command line entry,
we can add a couple of lines to our script to make use of the ``new_log`` function:

.. code-block:: python

   >>> import cmdline_provenance as cmdprov
   >>> my_log = cmdprov.new_log()
   >>> print(my_log)
   Tue Jun 26 11:24:46 2018: /Users/username/opt/anaconda3/bin/python ocean_analysis.py temperature_data.fmt salinity_data.fmt output.fmt

If our script is available via an online code hosting platform (e.g. GitHub, Bitbucket)
or has been published with a DOI,
we can include the relevant URL in the command log:

.. code-block:: python

   >>> my_log = cmdprov.new_log(code_url='https://doi.org/10.6084/m9.figshare.12143562.v3')
   >>> print(my_log)
   Tue Jun 26 11:24:46 2018: /Users/username/opt/anaconda3/bin/python ocean_analysis.py temperature_data.fmt salinity_data.fmt output.fmt (https://doi.org/10.6084/m9.figshare.12143562.v3)

If the code you've written to produce a given output file is in a Jupyter Notebook
rather than a command line script,
the ``new_log`` function will recognise it's being executed in a notebook
and adjust the log accordingly:

.. code-block:: python

   In [1]:  my_log = cmdprov.new_log()
            print(my_log)

   Out [1]: Tue Jun 26 11:24:46 2018: /Users/username/opt/anaconda3/bin/jupyter notebook ocean_analysis.ipynb


writing a log to file
^^^^^^^^^^^^^^^^^^^^^

If our output file is a self-describing file format (i.e. a format that carries its metadata with it),
then we can include our new log in the file metadata.
For instance, a common convention in weather and climate science is to include the command log
in the global history attribute of netCDF data files.
If we were using the `iris <https://scitools.org.uk/iris/docs/latest/>`_ library (for instance)
to read and write netCDF files using its cube data structure,
the process would look something like this:

.. code-block:: python

   >>> import iris
   >>> import cmdline_provenance as cmdprov
   >>> my_log = cmdprov.new_log()
   ...
   >>> type(cube)
   iris.cube.Cube
   >>> cube.attributes['history'] = my_log
   >>> iris.save(cube, 'output.nc')

Similarly, if our output file was a .png file created using 
`matplotlib <https://matplotlib.org/>`_,
we could append the command log to the image metadata:

.. code-block:: python

   >>> import matplotlib.pyplot as plt
   >>> my_log = cmdprov.new_log()
   ...
   >>> plt.savefig('output.png', metadata={'History': new_log})

The PyAOS Data Carpentry 
`lesson on data provenance <https://carpentrieslab.github.io/python-aos-lesson/09-provenance/index.html>`_
covers writing metadata to different image formats in more detail. 

If our output file is not a self-describing format (e.g. ``output.csv``),
then we can write a separate log file (i.e. a simple text file with the log in it)
using the ``write_log`` function.

.. code-block:: python

   >>> cmdprov.write_log('output.log', my_log)


While it's not a formal requirement of the ``write_log`` function,
it's good practice to make the name of the log file exactly the same as the name of the output file,
just with a different file extension (such as .log or .txt).

including logs from input files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to capture the complete provenance of the output file,
we need to include the command logs from the input files in our new log.
We can do this using the ``infile_logs`` keyword argument associated with the
``new_log`` function.

If our input files are a self-describing format,
then similar to the iris example above,
we can extract the input file logs from the metadata of the input files:

.. code-block:: python

   >>> inlogs = {}
   >>> inlogs['temperature_data.nc'] = temperature_cube.attributes['history']
   >>> inlogs['salinity_data.nc'] = salinity_cube.attributes['history']
   >>> my_log = cmdprov.new_log(infile_logs=inlogs)
   >>> print(my_log)
   Tue Jun 26 11:24:46 2018: /Users/username/opt/anaconda3/bin/python ocean_analysis.py temperature_data.nc salinity_data.nc output.nc
   History of temperature_data.nc:
   Tue Jun 26 09:24:03 2018: cdo daymean temperature_data.nc
   History of salinity_data.nc:
   Tue Jun 26 09:22:10 2018: cdo daymean salinity_data.nc
   Tue Jun 26 09:21:54 2018: ncatted -O -a standard_name,so,o,c,"ocean_salinity" salinity_data.nc

If the input files aren't self-describing,
we can use the ``read_log`` function to read the log files associated with the input data files
(these logs files may have been previously written using the ``write_log`` function):

.. code-block:: python

   >>> inlogs = {}
   >>> inlogs['temperature_data.csv'] = cmdprov.read_log('temperature_data.log')
   >>> inlogs['salinity_data.csv'] = cmdprov.read_log('salinity_data.log')
   >>> my_log = cmdprov.new_log(infile_history=inlogs)

For scripts that take many input files,
the resulting log files can become very long and unwieldy.
To help prevent this, think about ways to avoid repetition.
For instance, if you've got one input file that contains data from the year 1999-2003
and another equivalent file with data from 2004-2008,
it's probably only necessary to include the log from the 1999-2003 file
(i.e. because essentially identical data processing steps were taken to produce both files).  
