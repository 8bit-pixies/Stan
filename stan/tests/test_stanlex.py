# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 12:54:30 2014

@author: Chapman
"""

import unittest

#from SAS import saslexer as sasl

from stan.data import data_lex as stan_l

class TestMatch(unittest.TestCase):
#    expr_cases = (
#        ("data test; set test (rename=(a=b, c=d) drop = z); run;", ['1', '+', '2']),
#        )
#        
#    
#    def test_dataStepStmt(self):
#        for data, ans in self.expr_cases:
#            result = stan_l.dataStepStmt.parseString(data) != ''
#            self.assertTrue(result)
    
    def test_dataset_opt(self):
        self.assertTrue(stan_l.dataset_opt_stmt.parseString("") != '')
        self.assertTrue(stan_l.dataset_opt_stmt.parseString("(rename=(a=b))") != '')
        self.assertTrue(stan_l.dataset_opt_stmt.parseString("(rename=(a=b) drop=e)") != '')

if __name__ == '__main__':
    unittest.main()

