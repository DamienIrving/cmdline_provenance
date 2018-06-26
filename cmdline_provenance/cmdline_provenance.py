import os
import sys
import datetime
import git


def get_current_entry(repo_dir=None):
    """Create a record of the current command line entry.
    
    Args:
      repo_dir (str, optional) : location of git repository for the script
        that was executed at command line
    
    Returns:
      str : latest command line record
    
    """

    time_stamp = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")
    exe = sys.executable
    args = " ".join(sys.argv)
    
    if repo_dir:
        git_hash = git.Repo(repo_dir).heads[0].commit
        git_text = " (Git hash: %s)" %(str(git_hash)[0:7])
    else:
        git_text = ''
        
    entry = """%s: %s %s%s""" %(time_stamp, exe, args, git_text)
    
    return entry

    
def new_log(infile_history=None, extra_notes=None, repo_dir=None):
    """Create a new command line log/history.
    
    Args:
      infile_history (dict, optional) : A dictionary where keys are input filenames and values are 
        the command line log/history of those files 
      extra_notes (list, optional) : List containing character strings of extra information 
        (output is one list item per line)
      repo_dir (str, optional) : Location of git repository for the script that was executed
         at the command line (so that git hash can be included in updated history)
      
    Returns:
      str : complete updated command line log
      
    """
    
    log = ''
        
    current_entry = get_current_entry(repo_dir=repo_dir)
    log += current_entry + '\n'
    
    if extra_notes:
        log += 'Extra notes: \n'
        for line in extra_notes:
            log += line + '\n'
    
    if infile_history:
        assert type(infile_history) == dict
        nfiles = len(list(infile_history.keys()))
        for fname, history in infile_history.items():
            if nfiles > 1:
                log += 'History of %s: \n %s \n' %(fname, history)
            else:
                log += '%s \n' %(history)
    
    return log
    
    
def write_log(fname, cmd_log):
    """Write an updated command line log/history to a text file.
    
    Args:
      fname (str) : name of output file
      cmdlog (str) : command line log produced by new_log()
    
    """
   
    log_file = open(fname, 'w')
    log_file.write(cmd_log) 
    log_file.close()