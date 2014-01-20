#

from pyparsing import *
import functools

RESERVED_KEYWORDS = "by data proc quit set rename run drop keep".split()
SEMI_ = Suppress(";")

# define SAS reserved words
BY, DATA, PROC, QUIT, SET, RENAME, RUN, DROP, KEEP = map(functools.partial(Keyword, caseless=True),
                                    RESERVED_KEYWORDS)

ID_ = ~MatchFirst(map(functools.partial(Keyword, caseless=True), RESERVED_KEYWORDS)) + \
     Word(alphas+"_", alphanums+"_")



expr = PROC + ID_ + OPT_ + SEMI_ + \ 
    ZeroOrMore(EXPR) + \
    (RUN | QUIT)
    









# the proc expression is generally...

"""proc summary data = ...

statement .... /    options output;
;"""

# lets just try to parse proc freq first, 

"""proc freq data = df;
    tables sex;
run;"""

#this should translate to...
"""df.groupby(['Sex']).size()"""

## having a by statement first, would just do the following...
"""proc freq data = df;
    by group;
    tables sex;
run;
/*or this as well*/
proc freq data = df;
    tables group * sex;
run;
/*though not strictly the same, it would be a good idea, to say 
they are "equivalent" due to the multi index nature of Pandas...*/
"""

"""df.groupby(['Group','Sex']).size().reset_index()"""

