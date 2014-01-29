"""
The :mod:`stan.data_lex` module is the lexer for SAS-like language.
"""

from pyparsing import *
from .data_expr import EXPR_, ID_, DATA, SET, RENAME, RUN, DROP, KEEP, SEMI_, LOGICAL_
    
# set up logic
dataStepStmt = Forward()

# data/set inline options
rename_stmt = (OneOrMore(Group(ID_ + Suppress("=") + 
               ID_ ))).setResultsName('rename')
drop_stmt = OneOrMore( ID_ ).setResultsName('drop')
keep_stmt = OneOrMore( ID_ ).setResultsName('keep')

dataset_opt_stmt = Optional("("+ 
                        Optional(Suppress(RENAME) + "=" + "(" + rename_stmt + ")") + 
                        Optional(Suppress(DROP) + "=" + drop_stmt) +
                        Optional(Suppress(KEEP) + "=" + keep_stmt) +")")

# data step options (not inline)
opt_stmt = (
        (Suppress(RENAME) + rename_stmt + SEMI_) |
        (Suppress(KEEP) + keep_stmt + SEMI_) |
        (Suppress(DROP) + drop_stmt + SEMI_)
        #add by statement
    )


# data step logic
s_stmt = Group(ID_ + Suppress("=") + ( LOGICAL_.setResultsName('logical') | EXPR_ ) + SEMI_)
# data set statements

data_stmt = Group(Suppress(DATA) + ID_.setResultsName('name') + dataset_opt_stmt.setResultsName('data opt')).setResultsName('data') + SEMI_
set_stmt = Group(Suppress(SET) + ID_.setResultsName('name') + dataset_opt_stmt.setResultsName('set opt')).setResultsName('set') + SEMI_

dataStepStmt << (data_stmt + 
                 set_stmt + 
                 (ZeroOrMore(opt_stmt) &
                 ZeroOrMore(s_stmt).setResultsName('stmt')) + 
                 RUN + SEMI_)

