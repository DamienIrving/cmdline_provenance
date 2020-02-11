"""Utilities for capturing the history of commands used to produce a given output"""

from ._version import get_versions

__version__ = get_versions()['version']

del get_versions

from .cmdline_provenance import new_log
from .cmdline_provenance import read_log
from .cmdline_provenance import write_log

__all__ = [new_log, read_log, write_log]




