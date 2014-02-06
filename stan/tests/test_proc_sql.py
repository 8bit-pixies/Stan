# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 12:54:30 2014

@author: Chapman
"""

import unittest

from stan.transcompile import transcompile

cstr = """

proc sql;
    create table sample as 
    select test from a;
    quit;"""   

class TestDesc(unittest.TestCase):
    def test_dataset_opt(self):
        self.assertTrue(transcompile.transcompile(cstr) != "")

if __name__ == '__main__':
    unittest.main()