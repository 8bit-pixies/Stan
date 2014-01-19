# sas parse.py

from stanlex import dataStepStmt
import pandas as pd
from numpy import random

info = dataStepStmt.parseString("""data test;set df; run;""")

from pandas import DataFrame

df = DataFrame({
         'x': random.uniform(1., 168., 120),
         'y': random.uniform(7., 334., 120),
         'z': random.uniform(1.7, 20.7, 120),
         'month': [5,6,7,8]*30,
         'week': random.randint(1,4, 120)
     })

# figure out the parsing rules
"""data test;
set df; 
run;"""

#pandas solution
"""
test = df
"""

# simplest test case
print ''.join([info.data[0], "=", info.set[0]])

# figure out the parsing rules

#pandas solution
"""
test = df.rename(columns={"z": "b"})
"""

# you probably have to figure the keys first and then act accordingly, unfortunately in this format
# its difficult to know whether options refer to `data` or `set`

#info1.keys() <- using the keys determine how it should be parsed..

# also need to determine precedence, the easiest way might be to set up a class?
# to do precedence, one method might be to sort the the keys by precedence and used that as the 
# basis for ordering

# since you have a dict, you could just use a dict of functions....

# you would probably want to use decorators, since you will have the base thing and continually wrap things around it?
# ....or maybe not, since you just want to call functions down a stack

# or you could just have a list of try except, or get functions to determine it. 

# --------------------------------------------------------------------
# loose order

# 1. set statement options (inline)
# 2. Non-inline options
# 3. the statments in the order that is parsed
# 4. data statement options (inline)

cstr = """data test;
set df (rename=(z = b) drop= x y);
t = "chapman";
c = 1+2;
d = b+c;
na = substr(t,1,1) + "a";
run;"""

inf = dataStepStmt.parseString(cstr)

print "Loading..."

bd = inf.asDict()

print "Computing String...\n"

ss = ''
ss = bd['set']['name'][0]
data = bd['data']['name'][0]


def id_convert(v_ls, data):
    var_stmt = []
    for el in v_ls:
        try:            
            var_stmt.append("%s['%s']" % (data, el.id)) #if the expr is an identifier
        except:
            var_stmt.append(el)
    return ''.join(var_stmt)

# looking through set options
if len(bd['set'].keys()) == 0: 
    pass
else: 
    # check all the keys...
    for key in bd['set'].keys():
        if key == 'rename':
            #print bd['set']['rename']
            rename_ls = ",".join(["'%s':'%s'" % (x,y) for x,y in bd['set']['rename']])
            ss += '.rename(columns={%s})' % rename_ls
        if key == 'drop':
            drop_ls = ",".join(["'%s'" % x for x in bd['set']['drop']])
            ss += '.drop([%s],1)' % drop_ls
    ss = "%s=%s\n" % (data, ss)
    if 'logic_stmt' in bd.keys():
        for stmt in bd['logic_stmt']:
            print stmt
            var_stmt = id_convert(stmt[1:], data)
            ss += "%s['%s']=%s\n" % (data, stmt[0], var_stmt)
            

print "Soln is : \n\n", ss

