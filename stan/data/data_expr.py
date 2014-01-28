from pyparsing import *
import functools

RESERVED_KEYWORDS = "by data else if set then rename run drop keep".split()
SEMI_ = Suppress(";")

# define SAS reserved words
BY, DATA, ELSE, IF, SET, THEN, RENAME, RUN, DROP, KEEP = map(functools.partial(Keyword, caseless=True),
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
eq = Keyword("==") # change this otherwise statements like a = b = c can be confusing, since it would be a = (b == c)

ge = Keyword(">=")
gt = Keyword(">")
le = Keyword("<")
lt = Keyword("<=")
eq = Keyword("==") # change this otherwise statements like a = b = c can be confusing, since it would be a = (b == c)


lpar  = Literal( "(" )
rpar  = Literal( ")" )
addop  = plus | minus
multop = mult | div
logic = ge | gt | le | lt | eq
pi    = CaselessLiteral( "_PI_" )

EXPR_ = Forward()
LOGICAL_ = Forward()
LOGICAL_ << IF + EXPR_ + THEN + EXPR_ + Optional(ELSE + ((EXPR_ | LOGICAL_)))
FCALL_ = ID_ + "(" + Optional(EXPR_ + ZeroOrMore( "," + EXPR_ )) + ")"
atom = (FCALL_.setResultsName('fcall') | LOGICAL_.setResultsName('logical') | pi | NUM_ | STR_ | Group(ID_.setResultsName('id')) | (lpar + EXPR_ +rpar)) # deal with `a = -1` later

term = Forward()
term = atom + ZeroOrMore(( multop + EXPR_ ))
log = term + ZeroOrMore(( addop + EXPR_ ))
EXPR_ << log + ZeroOrMore(( logic + EXPR_ ))

LOGICAL_ = Forward()
LOGICAL_ << IF + Group(EXPR_).setResultsName('l_cond') + THEN + Group(EXPR_).setResultsName('l_result') + Group(Optional(ELSE.suppress() + (LOGICAL_ | EXPR_))).setResultsName('r_cond')




















