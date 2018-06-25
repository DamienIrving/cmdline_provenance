# Command line provenance

`cmdline_provenance` is a Python package for keeping track of your data processing steps.

It was inspired by the popular [NCO](http://nco.sourceforge.net/)
and [CDO](https://code.mpimet.mpg.de/projects/cdo) command line tools,
which automatically generate a record of what was executed at the command line,
append that record to the history attribute from the input (netCDF) data file,
and then set the new extended record as the history attribute of the output (netCDF) data file.

For example, after selecting the 2001-2005 time period from a rainfall data file
and then deleting the `long_name` file attribute,
the command log would look as follows:
```
Fri Dec 08 10:05:47 2017: ncatted -O -a long_name,pr,d,, rainfall_data_200101-200512.nc
Fri Dec 01 07:59:16 2017: cdo seldate,2001-01-01,2005-12-31 rainfall_data_185001-200512.nc rainfall_data_200101-200512.nc
```
Following this simple approach to data provenance,
it is possible maintain a record of all data processing steps
from intial download/creation of your data files to the end result (e.g. a .png image).

`cmdline_provenance` contains a series of functions for generating history records in the NCO/CDO format,
and for combining the current record with previous records to maintain a complete command log.

## Documentation

http://cmdline-provenance.readthedocs.io/en/latest/

## Installation

```
pip install cmdline-provenance
```
