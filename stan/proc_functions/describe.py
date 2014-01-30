"""
The :mod:`stan.proc_functions.describe` module is the proc describe function
"""

def describe(data, by):
    return data.groupby(by).describe()  
