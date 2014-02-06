"""
The :mod:`stan.transcompile` module is the key module to convert a full script and run it
"""

import re

from stan.data.data_parse import data_parse
from stan.proc.proc_parse import proc_parse


def transcompile(cstr):
    """transcompile converts a stan script to python equivalent
    
    Parameters
    ----------
    
    cstr : the stan script in string format
    
    Notes 
    -----
    
    Comments are stripped out first, and then all python code is ignored.
    
    Multi-line comments start with ``/*`` and end with ``*/``
    Single line comments start with ``*`` and end with ``;`` or start with ``//``
    Python code begin with ``#``
    
    """
    multi_comments = re.compile(r'/\*.*?\*/', re.DOTALL)
    single_c_comments = re.compile(r'//.*?')
    single_sas_comments = re.compile(r'\*.*?;')
    pycode = re.compile(r'#[ ]?')
    
    cstr = multi_comments.sub(r' ', cstr)
    cstr = single_c_comments.sub(r' ', cstr)
    cstr = single_sas_comments.sub(r' ', cstr)    
    cstr = pycode.sub(r'', cstr)    
    
    
    find_rule = re.compile(r'(((?:data)|(?:proc)).*?(?:(?:run|quit)\s*;))', re.I | re.DOTALL)
    
    def replace_in_script(f_array):
        if f_array.group(2).lower() == 'data':
            return data_parse(f_array.group(1))
        elif f_array.group(2).lower() == 'proc':
            return proc_parse(f_array.group(1))
        else:
            raise "invalid code found"
    
    ss = re.sub(find_rule, replace_in_script, cstr)
           
    return re.sub(r'\n+', '\n', ss)
