"""
The :mod:`stan.proc.proc_parse` module is the proc parser for SAS-like language.
"""

from .proc_expr import RESERVED_KEYWORDS, PROC_
from ..proc_functions import * 

def proc_parse(cstr):
    """proc parse converts procedure statements to python function equivalents
    
    Parameters
    ----------
    
    v_ls : list of tokens
    
    Notes 
    -----
    
    ``data`` and ``output``/``out`` are protected variables.    
    """
    v_ls = PROC_.parseString(cstr)
    
    sls = []
    preprend = ''
        
    for ls in v_ls[1:]:        
        if len(ls[1:]) > 1:
            sls.append("%s=['%s']" % (ls[0], "','".join(ls[1:])))
        else:
            if ls[0] in ['data']:
                sls.append("%s=%s" % (ls[0], ls[1]))
            elif ls[0] in ['output', 'out']:
                preprend += '%s=' % ls[1]
            else:
                sls.append("%s='%s'" % (ls[0], ls[1]))
    return '%s%s.%s(%s)' % (preprend, v_ls[0], v_ls[0], ','.join(sls)) # this statement is a bit dodgy



