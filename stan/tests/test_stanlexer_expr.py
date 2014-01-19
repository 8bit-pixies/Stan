#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

#from SAS import saslexer as sasl

from stan import stanlexer_expr as stan_e

class TestMatch(unittest.TestCase):
    expr_cases = (
        ("1+2", ['1', '+', '2']),
        ("'Chapman'", ["Chapman"]),
        ("substr(Name, 1,1)", [['substr', ['Name', '1', '1']]])
        )
        
    
    def test_exprTest(self):
        for data, ans in self.expr_cases:
            result = stan_e.expr.parseString(data)
            self.assertEqual(result.asList(), ans)

if __name__ == '__main__':
    unittest.main()

