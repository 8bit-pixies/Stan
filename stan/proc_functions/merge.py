"""
The :mod:`stan.proc_functions.merge` module is the proc merge function
"""

def merge(dt_left, dt_right, how='inner', on=None, left_on=None, right_on=None, left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'), copy=True):
    return dt_left.merge(dt_right, how='inner', on=None, left_on=None, right_on=None, left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'), copy=True)
