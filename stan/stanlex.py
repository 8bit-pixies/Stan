# sasplex.py
#
# mirror simple SQL format



from pyparsing import *
import functools
from stanexpr import expr as EXPR_

# define SAS tokens
    
RESERVED_KEYWORDS = "data set rename run drop keep".split()
SEMI_ = Suppress(";")

DATA, SET, RENAME, RUN, DROP, KEEP = map(functools.partial(Keyword, caseless=True),
                                    RESERVED_KEYWORDS)
ID_ = ~MatchFirst(map(functools.partial(Keyword, caseless=True), RESERVED_KEYWORDS)) + \
     Word(alphas+"_", alphanums+"_")
point = Literal( "." )
fnumber = Combine(Word(nums) + Optional( point + Optional( Word(nums))))

# set up logic
dataStepStmt = Forward()

# data/set inline options
rename_stmt = (OneOrMore(Group(ID_ + Suppress("=") + 
               ID_ ))).setResultsName('rename')
drop_stmt = OneOrMore( ID_ ).setResultsName('drop')
keep_stmt = OneOrMore( ID_ ).setResultsName('keep')

dataset_opt_stmt = Optional("("+ 
                        Optional(RENAME + "=" + "(" + rename_stmt + ")") + 
                        Optional(DROP + "=" + drop_stmt) +
                        Optional(KEEP + "=" + keep_stmt) +")")

# data step options (not inline)

opt_stmt = (
        (RENAME + rename_stmt + SEMI_) |
        (KEEP + keep_stmt + SEMI_) |
        (DROP + drop_stmt + SEMI_)
        #add by statement
    )


# logic
s_stmt = Group(ID_ + Suppress("=") + EXPR_ + SEMI_)
# data set statements

data_stmt = Group(Suppress(DATA) + ID_.setResultsName('name') + dataset_opt_stmt.setResultsName('data opt')).setResultsName('data') + SEMI_
set_stmt = Group(Suppress(SET) + ID_.setResultsName('name') + dataset_opt_stmt.setResultsName('set opt')).setResultsName('set') + SEMI_

dataStepStmt << (data_stmt + 
                 set_stmt + 
                 ZeroOrMore(opt_stmt) + 
                 (ZeroOrMore(s_stmt)).setResultsName('logic_stmt') + 
                 RUN + SEMI_)

#dataStepStmt.validate()

#def test(s):
#    print s, "->"
#    print dataStepStmt.parseString(s)
#    # insert stuff...

#test("""data test (rename=(a = b));
#set test (drop= a b c); 
#run;""")

#test("data test; set test;run;")
#test("data test; set test; name = 1+2; run;")
#test('''data test; set test; t = "Chapman"; run;''')
#test('''data test; set test; t = substr("Chapman",1,3); run;''')

# set as dict



