"""
The :mod:`stan.transcompile` module is the key module to convert a full script and run it
"""

import re

from stan.data.data_parse import data_parse
from stan.proc.proc_parse import proc_parse


def transcompile(cstr):
    find_rule = re.compile(r'(((?:data)|(?:proc)).*?(run\s*;))', re.I | re.DOTALL)
    f_all = find_rule.findall(cstr)
    
    ss = ''
    for code in f_all:
        if code[1].strip().lower() == 'data':
            ss += '%s\n' % data_parse(code[0])
        elif code[1].strip().lower() == 'proc':
            ss += '%s\n' % proc_parse(code[0])
        else:
            raise "invalid code found"
    
    return re.sub(r'\n+', '\n', ss)

