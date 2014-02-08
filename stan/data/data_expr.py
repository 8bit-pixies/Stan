"""
The :mod:`stan.data.data_expr` module is the grammar for SAS-like language.
"""

from pyparsing import *
import functools

RESERVED_KEYWORDS = "by data do else end if set then rename run drop keep".split()
SEMI_ = Suppress(";")

# define SAS reserved words
BY, DATA, DO, ELSE, END, IF, SET, THEN, RENAME, RUN, DROP, KEEP = map(functools.partial(Keyword, caseless=True),
                                    RESERVED_KEYWORDS)
ID_ = ~MatchFirst(map(functools.partial(Keyword, caseless=True), RESERVED_KEYWORDS)) + \
     Word(alphas+"_", alphanums+"_")

NUM_ = Combine(Optional("-") + Word(nums) + Optional( Literal( "." ) + Optional( Word(nums)))).setResultsName('num_type')
 
STR_ = (QuotedString(quoteChar="'", escChar='\\', multiline=True, unquoteResults=False) | 
        QuotedString(quoteChar='"', escChar='\\', multiline=True, unquoteResults=False)).setResultsName('str_type')

# define ops
plus  = Literal( "+" )
minus = Literal( "-" )
mult  = Literal( "*" )
div   = Literal( "/" )

mod = Keyword("%")

ge = Keyword(">=")
gt = Keyword(">")
le = Keyword("<")
lt = Keyword("<=")
eq = Keyword("=") # change this otherwise statements like a = b = c can be confusing, since it would be a = (b == c)

lpar  = Literal( "(" )
rpar  = Literal( ")" )
addop  = plus | minus
multop = mult | div
otherop = mod
logic = ge | gt | le | lt | eq
pi    = CaselessLiteral( "_PI_" )

EXPR_ = Forward()
FCALL_ = ID_ + "(" + Optional(EXPR_ + ZeroOrMore( "," + EXPR_ )) + ")"
atom = (FCALL_.setResultsName('fcall') | pi | NUM_ | STR_ | Group(ID_.setResultsName('id')) | (lpar + EXPR_ +rpar))

term = Forward()
term = atom + ZeroOrMore(( multop + EXPR_ ))
EXPR_ << term + ZeroOrMore(( addop + EXPR_ )) + ZeroOrMore(( otherop + EXPR_ ))
#

# the logical statement may need to be changed in the future to support the way sas handles it, particularly the "if then do end" pattern
# SAS Logical specific expressions

SEXPR_ = EXPR_ + ZeroOrMore(( logic + EXPR_ ))

DOEXPR = (ID_ + Suppress("=") + EXPR_ + SEMI_).setResultsName('singleExpr') | (Suppress(DO) + SEMI_ + OneOrMore(Group(ID_ + Suppress("=") + EXPR_) + SEMI_) + Suppress(END) + SEMI_)

SASLOGICAL_ = Forward()
SASLOGICAL_ << Group(IF + Group(SEXPR_).setResultsName('l_cond') + THEN + Group(DOEXPR).setResultsName('assign')  + Group(Optional(ELSE.suppress() + (SASLOGICAL_ | Group(DOEXPR).setResultsName('assign')))).setResultsName('r_cond'))
