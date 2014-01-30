# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 12:54:30 2014

@author: Chapman
"""

import unittest

from stan.proc import proc_parse
from pandas import DataFrame
from stan.proc_functions import describe

cstr = """proc describe data = df1 out = df2;
        by a;
        run;"""    

df1 = DataFrame({'a' : [1, 0, 1], 'b' : [0, 1, 1] }, dtype=bool)

class TestDesc(unittest.TestCase):
    def test_dataset_opt(self):
        torun = proc_parse.proc_parse(cstr).strip()
        self.assertTrue(torun == "df2=describe.describe(data=df1,by='a')")
        exec(torun)
        self.assertTrue(len(df2.columns) > 1)

if __name__ == '__main__':
    unittest.main()
