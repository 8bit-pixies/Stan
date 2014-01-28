# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 12:54:30 2014

@author: Chapman
"""

import unittest

from stan.data import data_parse as stan_p
from stan.data.data_lex import dataStepStmt
import pandas as pd
from numpy import random

from pandas import DataFrame

info = dataStepStmt.parseString("""data test;set df; run;""")

df = DataFrame({
         'x': random.uniform(1., 168., 120),
         'y': random.uniform(7., 334., 120),
         'z': random.uniform(1.7, 20.7, 120),
         'month': [5,6,7,8]*30,
         'week': random.randint(1,4, 120)
     })

cstr = """data test(rename=(b = z));
set df (rename=(z = b) drop= x y);
t = "chapman";
g = -1;
c = 1+2;
d = b+c;
na = substr(t,1,1) + "a";
halfyr = if month < (6*180) then 1 else if month > (6*180) then 2 else 0;
run;"""


def substr(ss, start, length):
    return ss[start-1:start+length-1]

	
class TestMatch(unittest.TestCase):
           
    
    def test_exprTest(self):
        estr = stan_p.stan(cstr)
        exec(estr)
        self.assertTrue(len(test.columns) > 1)
        

if __name__ == '__main__':
    unittest.main()