#

from pyparsing import *
import functools

RESERVED_KEYWORDS = "data proc rename run drop keep".split()
SEMI_ = Suppress(";")

# define SAS reserved words
DATA, PROC, RENAME, RUN, DROP, KEEP = map(functools.partial(Keyword, caseless=True),
                                    RESERVED_KEYWORDS)

ID_ = ~MatchFirst(map(functools.partial(Keyword, caseless=True), RESERVED_KEYWORDS)) + \
     Word(alphas+"_", alphanums+"_")

PROC_ = Forward()

PROC_ << (PROC + ID_ + SEMI_ +  
          ZeroOrMore(ID_ + Group(Optional(Suppress("=")) + OneOrMore(ID_) + SEMI_)) +
          RUN + SEMI_) # this needs to be generic enough to handle unseen IDs before

dd = PROC_.parseString("""proc describe ;
    by week month;  var x;
run;""")

# should be able to handle merges and stuff, try a proc merge
from pandas import DataFrame
import pandas as pd

left = DataFrame({'key': ['foo', 'foo'], 'lval': [1, 2]})
right = DataFrame({'key': ['foo', 'foo'], 'rval': [4, 5]})

pd.merge(left, right, on='key')

