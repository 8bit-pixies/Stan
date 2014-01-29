"""
The :mod:`stan.proc.proc_parse` module is the proc parser for SAS-like language.
"""

from __future__ import absolute_import

from .proc_expr import RESERVED_KEYWORDS, PROC_
from ..proc_functions.describe import * 

cstr = """proc describe data = df1 out=df2;
by a;
run;"""

#def describe(data, by):
#    return data.groupby(by).describe()  

def proc_args(v_ls):
    """proc args converts procedure statements to python function equivalents
    
    Parameters
    ----------
    
    v_ls : list of tokens
    
    Notes 
    -----
    
    ``data`` and ``output``/``out`` are protected variables.    
    """
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
    return '%s%s(%s)' % (preprend, v_ls[0], ','.join(sls))

dd = PROC_.parseString(cstr)
ss = proc_args(dd)

from pandas import DataFrame
df1 = DataFrame({'a' : [1, 0, 1], 'b' : [0, 1, 1] }, dtype=bool)
exec(ss)

