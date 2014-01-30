# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 12:54:30 2014

@author: Chapman
"""

import unittest

from stan.proc import proc_parse
from pandas import DataFrame
from stan.proc_functions import merge

cstr = """proc merge out = df2;
        dt_left left;
        dt_right right;
        on = 'key';
        run;"""    

left = DataFrame({'key': ['foo', 'foo'], 'lval': [1, 2]})
right = DataFrame({'key': ['foo', 'foo'], 'rval': [4, 5]})

class TestDesc(unittest.TestCase):
    def test_dataset_opt(self):
        left = DataFrame({'key': ['foo', 'foo'], 'lval': [1, 2]})
        right = DataFrame({'key': ['foo', 'foo'], 'rval': [4, 5]})
        
        torun = proc_parse.proc_parse(cstr).strip()
        self.assertTrue(torun == "df2=merge.merge(dt_left=left,dt_right=right,on='key')")
        exec(torun)
        self.assertTrue(len(df2.columns) > 1)

if __name__ == '__main__':
    unittest.main()
