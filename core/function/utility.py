"""
Define some utility functions.
"""
import os

def which(exe_name: str) -> bool:
    
    ok = False
    ok = os.path.isfile(exe_name) and os.access(exe_name, os.X_OK)
    if ok:
        return True
    fpath = os.environ["PATH"].split(os.pathsep)
    for path in fpath:
        exe_file = os.path.join(path, exe_name)
        if os.path.isfile(exe_file) and os.access(exe_file, os.X_OK):
            return True
    return False

