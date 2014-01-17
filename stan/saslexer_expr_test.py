import unittest

#from SAS import saslexer as sasl
import os
import sys
sys.path.append('H:/My Documents/Scripts/SAS-py/SASpy/SAS')

import saslexer_expr as sase

class TestMatch(unittest.TestCase):
    expr_cases = (
        ("1+2", ['1', '+', '2']),
        ("'Chapman'", ["Chapman"]),
        ("substr(Name, 1,1)", [['substr', ['Name', '1', '1']]])
        )
        
    
    def test_exprTest(self):
        for data, ans in self.expr_cases:
            result = sase.expr.parseString(data)
            self.assertEqual(result.asList(), ans)

unittest.main()
