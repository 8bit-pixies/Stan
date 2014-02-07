#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

#from SAS import saslexer as sasl

from stan.data import data_expr as stan_e

class TestMatch(unittest.TestCase):
    expr_cases = (
        ("1+2", ['1', '+', '2']),
        ("'Chapman'", ["'Chapman'"]),
        ("substr(Name, 1,1)", ['substr', '(', ['Name'], ',', '1', ',', '1', ')'])
        )
        
    
    def test_exprTest(self):
        for data, ans in self.expr_cases:
            result = stan_e.EXPR_.parseString(data)
            self.assertEqual(result.asList(), ans)

class TestSASLogical(unittest.TestCase):
    ss = """if a = 1 then a = 2;"""
    sd = """if a = 1 then do;
    b = 1;
    c = 2;
    end;
    else if a = 2 then do;
    b =2;
    end;
    else c = 1;
    """
    
    def test_exprTest(self):
        #self.assertTrue(stan_e.SASLOGICAL_.parseString(self.ss) != '')
        #self.assertEqual(stan_e.SASLOGICAL_.parseString(self.ss), '')
        #self.assertEqual(stan_e.SASLOGICAL_.parseString(self.sd), '')
        None
            
if __name__ == '__main__':
    unittest.main()

