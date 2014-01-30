"""
The :mod:`stan.proc.proc_parse` module is the proc parser for SAS-like language.
"""

from stan.proc.proc_expr import RESERVED_KEYWORDS, PROC_
from stan.proc_functions import * 

def proc_parse(cstr):
    """proc parse converts procedure statements to python function equivalents
    
    Parameters
    ----------
    
    v_ls : list of tokens
    
    Notes 
    -----
    
    ``data`` and ``output``/``out`` are protected variables.    
    If you wish to use a DataFrame as an argument, prepend ``dt_`` for the parser to interpret this correctly
    """
    v_ls = PROC_.parseString(cstr)
    
    sls = []
    preprend = ''
        
    for ls in v_ls[1:]:        
        if len(ls[1:]) > 1:
            sls.append("%s=['%s']" % (ls[0], "','".join(ls[1:])))
        else:
            if ls[0].startswith('dt_') or ls[0] in ['data']: # hungarian notation if we want to use DataFrame as a variable
                sls.append("%s=%s" % (ls[0], ls[1]))
            elif ls[0] in ['output', 'out']:
                preprend += '%s=' % ls[1]
            else:
                sls.append("%s='%s'" % (ls[0], ls[1]))
    return '%s%s.%s(%s)' % (preprend, v_ls[0], v_ls[0], ','.join(sls)) # this statement is a bit dodgy



