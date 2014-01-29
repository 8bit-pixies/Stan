"""
The :mod:`stan.proc.proc_parse` module is the proc parser for SAS-like language.
"""

from proc_expr import RESERVED_KEYWORDS, PROC_

cstr = """proc describe data = test;
    by sex;
   run;"""

dd = PROC_.parseString(cstr)

ss = ''

# this is the function we're running

def get_args(v_ls):
    sls = []
    for ls in v_ls:        
        if len(ls[1:]) > 1:
            sls.append("%s=['%s']" % (ls[0], "','".join(ls[1:])))
        else:
            if ls[0] in ['data', 'output', 'out']:
                sls.append("%s=%s" % (ls[0], ls[1]))
            else:
                sls.append("%s='%s'" % (ls[0], ls[1]))
    return ",".join(sls)


ss = '%s(%s)' % (dd[0], get_args(dd[1:]))

from pandas import DataFrame

df1 = DataFrame({'a' : [1, 0, 1], 'b' : [0, 1, 1] }, dtype=bool)

#df1 = DataFrame({'a' : [1, 0, 1], 'b' : [0, 1, 1] }, dtype=bool)

def describe(data, by):
    return data.groupby(by).describe()  
