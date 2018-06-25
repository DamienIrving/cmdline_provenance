import os
import sys
import datetime
import git


def new_cmdline_history(repo_dir=None):
    """Create a new history record.
    
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

    
def update_history(file_info=None, extra_notes=None, repo_dir=None):
    """Update command line history.
    
    Args:
      file_info (dict, optional) : A dictionary where keys are input filenames and values are 
        the command line history of those files 
      extra_notes (list, optional) : List containing character strings of extra information 
        (output is one list item per line)
      repo_dir (str, optional) : Location of git repository for the script that was executed
         at the command line (so that git hash can be included in updated history)
      
    Returns:
      str : complete updated command line history
      
    """
    
    output = ''
        
    # Write the newest command line entry
    new_history = new_cmdline_history(repo_dir=repo_dir)
    output += new_history + '\n'
    
    # Write the extra info
    if extra_notes:
        output += 'Extra notes: \n'
        for line in extra_notes:
            output += line + '\n'
    
    # Write the file details
    if file_info:
        assert type(file_info) == dict
        nfiles = len(list(file_info.keys()))
        for fname, history in file_info.items():
            if nfiles > 1:
                output += 'History of %s: \n %s \n' %(fname, history)
            else:
                output += '%s \n' %(history)
    
    return output
    
    
def write_history_txt(fname, file_info=None, extra_notes=None, repo_dir=None):
    """Write an updated command line history to a text file.
    
    Args:
      file_info (dict, optional) : A dictionary where keys are input filenames and values are 
        the command line history of those files 
      extra_notes (list, optional) : List containing character strings of extra information 
        (output is one list item per line)
      repo_dir (str, optional) : Location of git repository for the script that was executed
         at the command line (so that git hash can be included in updated history)
    
    """
   
    complete_history = update_history(file_info=file_info, extra_notes=extra_notes, repo_dir=repo_dir)
   
    history_file = open(fname, 'w')
    history_file.write(complete_history) 
    history_file.close()