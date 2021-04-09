import os
import sys
import datetime


def get_current_entry(code_url=None):
    """Create a record of the current command line entry.
    
    Kwargs:
      code_url (str):  Where to find the code online
                       (e.g. https://github.com/... or https://doi.org/...) 
    
    Returns:
      str. Latest command line record
    
    """

    time_stamp = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")
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
    
    log = ''
        
    current_entry = get_current_entry(code_url=code_url)
    log += current_entry + '\n'
    
    if extra_notes:
        log += 'Extra notes: \n'
        for line in extra_notes:
            log += line + '\n'
    
    if infile_logs:
        assert type(infile_logs) == dict, \
        "infile_logs argument must be a dict: file names as keys and logs as values"
        nfiles = len(list(infile_logs.keys()))
        for fname, history in infile_logs.items():
            if nfiles > 1:
                log += f"History of {fname}: \n {history} \n"
            else:
                log += f"{history} \n"
    
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