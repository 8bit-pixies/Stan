"""
The :mod:`stan.proc_functions.to_csv` module converts a dataframe object to csv. See Pandas documentation for more information.
"""

import pandas as pd

def to_csv(data, path_or_buf, sep=', ', na_rep='', float_format=None, cols=None, header=True, index=True, index_label=None, mode='w', nanRep=None, encoding=None, quoting=None, line_terminator='n', chunksize=None, tupleize_cols=False, date_format=None, **kwds):
    return data.to_csv(path_or_buf, sep=', ', na_rep='', float_format=None, cols=None, header=True, index=True, index_label=None, mode='w', nanRep=None, encoding=None, quoting=None, line_terminator='n', chunksize=None, tupleize_cols=False, date_format=None, **kwds)
    
