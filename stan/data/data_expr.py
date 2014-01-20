from pyparsing import *
import functools

RESERVED_KEYWORDS = "by data set rename run drop keep".split()
SEMI_ = Suppress(";")

# define SAS reserved words
BY, DATA, SET, RENAME, RUN, DROP, KEEP = map(functools.partial(Keyword, caseless=True),
                                    RESERVED_KEYWORDS)
ID_ = ~MatchFirst(map(functools.partial(Keyword, caseless=True), RESERVED_KEYWORDS)) + \
     Word(alphas+"_", alphanums+"_")

NUM_ = Combine(Word(nums) + Optional( Literal( "." ) + Optional( Word(nums)))).setResultsName('num_type')
 
STR_ = (QuotedString(quoteChar="'", escChar='\\', multiline=True, unquoteResults=False) | 
        QuotedString(quoteChar='"', escChar='\\', multiline=True, unquoteResults=False)).setResultsName('str_type')

# define ops
plus  = Literal( "+" )
minus = Literal( "-" )
mult  = Literal( "*" )
div   = Literal( "/" )
lpar  = Literal( "(" ).suppress()
rpar  = Literal( ")" ).suppress()
addop  = plus | minus
multop = mult | div
pi    = CaselessLiteral( "_PI_" )

EXPR_ = Forward()
FCALL_ = ID_ + "(" + Optional(EXPR_ + ZeroOrMore( "," + EXPR_ )) + ")"
atom = (FCALL_.setResultsName('fcall') | pi | NUM_ | STR_ | Group(ID_.setResultsName('id')) | (lpar + EXPR_ +rpar)) # deal with `a = -1` later

term = Forward()
term = atom + ZeroOrMore(( multop + EXPR_ ))
EXPR_ << term + ZeroOrMore(( addop + EXPR_ ))
