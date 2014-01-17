# sas parse.py

from saslex import dataStepStmt
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
inf = dataStepStmt.parseString("""data test (drop= a b);
set df (rename=(z = b e=v)); 
run;""")

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

print "Loading..."

bd = inf.asDict()

print "Computing String"

ss = ''
ss = bd['set']['name'][0]

# looking through set options
if len(bd['set'].keys()) == 0: 
    pass
else: 
    # check all the keys...
    for key in bd['set'].keys():
        if key == 'rename':
            rename_ls = ",".join(["'%s':'%s'" % (x,y) for x,y in bd['set']['rename']])
            ss = ss+'.rename(columns={%s})' % (rename_ls)
        if key == 'drop':
            pass


print "Soln is : ", ss

