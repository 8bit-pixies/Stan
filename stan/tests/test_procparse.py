# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 12:54:30 2014

@author: Chapman
"""

import unittest

from stan.proc import proc_parse

cstr = """proc describe data = df1 out = df2;
        by a;
        run;"""   

cstr1 = """proc describe data = df1 out = df2;
    by a;
    fin = "/usr/test.text";
run;"""

class TestDesc(unittest.TestCase):
    def test_dataset_opt(self):
        self.assertTrue(proc_parse.proc_parse(cstr).strip() == "df2=describe.describe(data=df1,by='a')")
        self.assertTrue(proc_parse.proc_parse(cstr1).strip() == "df2=describe.describe(data=df1,by='a',fin='/usr/test.text')")

if __name__ == '__main__':
    unittest.main()
