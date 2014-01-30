"""
The :mod:`stan.stan` module is the key module to convert a full script and run it
"""

import sys
import re

from .proc.proc_parse import proc_parse
from .data.data_parse import data_parse

def transcompile(cstr):
    find_rule = re.compile(r'(((?:data)|(?:proc)).*?(run\s*;))', re.I | re.DOTALL)
    f_all = find_rule.findall(cstr)
    for x in  f_all:
        print x[0]
    
    ss = ''
    for code in f_all:
        if code[1].strip().lower() == 'data':
            print ss
            ss += '\n%s\n' % data_parse(code[0])
        elif code[1].strip().lower() == 'proc':
            print ss
            ss += '\n%s\n' % proc_parse(code[0])
        else:
            raise error("invalid code found")
    
    return ss


cstr = """
Data test;
    set test;
  run;
  
proc describe data = test out = test;
    by sex;
    var age;
run;

data test1;
    set test;
run;

"""
print transcompile(cstr)