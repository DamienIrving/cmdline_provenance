import os
import sys
import datetime
import subprocess

import ipynbname


def isnotebook():
    try:
        ipynbname.name()
        return True
    except FileNotFoundError:
        return False


def get_current_entry(code_url=None):
    """Create a record of the current command line entry.
    
    Kwargs:
      code_url (str):  Where to find the code online
                       (e.g. https://github.com/... or https://doi.org/...)
    
    Returns:
      str. Latest command line record
    
    """

    time_stamp = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")
    if isnotebook():
        exe = subprocess.run(['which', 'jupyter'], stdout=subprocess.PIPE)
        exe = exe.stdout.decode('utf-8').replace('\n','')
        args = " ".join(['notebook', str(ipynbname.path())])
    else:
        exe = sys.executable
        args = " ".join(sys.argv)
    
    entry = f"{time_stamp}: {exe} {args}"
    if code_url:
        entry = entry + f" ({code_url})"
            
    return entry

    
def new_log(infile_logs=None, extra_notes=None, code_url=None):
    """Create a new command log/history.
    
    Kwargs:
      infile_logs (dict):  Keys are input file names
                           Values are the logs for those files 
      extra_notes (list):  Extra information to include in new log
                           (output is one list item per line)
      code_url (str):      Where to find the code online
                           (e.g. https://github.com/... or https://doi.org/...) 
      
    Returns:
      str. Command log
      
    """
    
    log = get_current_entry(code_url=code_url)
    
    if extra_notes:
        assert isinstance(extra_notes, (list, tuple)), \
        "extra_notes must be a list/tuple: output is one list/tuple item per line"
        log += '\nExtra notes: '
        for line in extra_notes:
            log += '\n' + line 
    
    if infile_logs:
        assert isinstance(infile_logs, dict), \
        "infile_logs must be a dict: file names as keys and logs as values"
        nfiles = len(list(infile_logs.keys()))
        for fname, history in infile_logs.items():
            if nfiles > 1:
                log += f"\nHistory of {fname}: \n {history}"
            else:
                log += f"\n{history}"
    
    return log


def read_log(fname):
    """Read a log file.
    
    Args:
      fname (str):  Name of log file
      
    Returns:
      str. Command log
    
    """
   
    log_file = open(fname, 'r')
    log = log_file.read()
    
    return log

    
def write_log(fname, cmd_log):
    """Write an updated command log/history to a text file.
    
    Args:
      fname (str):    Name of output file
      cmd_log (str):  Command line log produced by new_log()
    
    """
   
    log_file = open(fname, 'w')
    log_file.write(cmd_log) 
    log_file.close()