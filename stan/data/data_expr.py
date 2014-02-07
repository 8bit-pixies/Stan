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

ge = Keyword(">=")
gt = Keyword(">")
le = Keyword("<")
lt = Keyword("<=")
eq = Keyword("=") # change this otherwise statements like a = b = c can be confusing, since it would be a = (b == c)

lpar  = Literal( "(" )
rpar  = Literal( ")" )
addop  = plus | minus
multop = mult | div
logic = ge | gt | le | lt | eq
pi    = CaselessLiteral( "_PI_" )

EXPR_ = Forward()
FCALL_ = ID_ + "(" + Optional(EXPR_ + ZeroOrMore( "," + EXPR_ )) + ")"
atom = (FCALL_.setResultsName('fcall') | pi | NUM_ | STR_ | Group(ID_.setResultsName('id')) | (lpar + EXPR_ +rpar))

term = Forward()
term = atom + ZeroOrMore(( multop + EXPR_ ))
log = term + ZeroOrMore(( addop + EXPR_ ))
EXPR_ << log + ZeroOrMore(( logic + EXPR_ ))

# the logical statement may need to be changed in the future to support the way sas handles it, particularly the "if then do end" pattern

# SAS Logical specific expressions

DOEXPR = (ID_ + Suppress("=") + EXPR_ + SEMI_) | (DO + SEMI_ + OneOrMore(ID_ + Suppress("=") + EXPR_ + SEMI_) + END + SEMI_)

SASLOGICAL_ = Forward()
SASLOGICAL_ << IF + Group(EXPR_).setResultsName('l_cond') + THEN + DOEXPR  + Group(Optional(ELSE.suppress() + (LOGICAL_ | DOEXPR))).setResultsName('r_cond')


