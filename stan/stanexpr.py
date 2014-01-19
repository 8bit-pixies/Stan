from pyparsing import *
#from stanlexer_fcall import expr as FCALL_

point = Literal( "." )
fnumber = Combine(Word(nums) + Optional( point + Optional( Word(nums)))).setResultsName('num_type')
 
ID_ = Word(alphas+'_', alphanums)
STR_ = (QuotedString(quoteChar="'", escChar='\\', multiline=True, unquoteResults=False) | 
        QuotedString(quoteChar='"', escChar='\\', multiline=True, unquoteResults=False)).setResultsName('str_type')
    
 
plus  = Literal( "+" )
minus = Literal( "-" )
mult  = Literal( "*" )
div   = Literal( "/" )
lpar  = Literal( "(" ).suppress()
rpar  = Literal( ")" ).suppress()
addop  = plus | minus
multop = mult | div
#expop = Literal( "^" )
pi    = CaselessLiteral( "_PI_" )

expr = Forward()
FCALL_ = ID_ + "(" + Optional(expr + ZeroOrMore( "," + expr )) + ")"
atom = (FCALL_.setResultsName('fcall') | pi | fnumber | STR_ | Group(ID_.setResultsName('id')) | (lpar + expr +rpar)) # deal with `a = -1` later

# by defining exponentiation as "atom [ ^ factor ]..." instead of "atom [ ^ atom ]...", we get right-to-left exponents, instead of left-to-righ
# that is, 2^3^2 = 2^(3^2), not (2^3)^2.
#factor = Forward()
#factor << atom + ZeroOrMore( ( expop + factor ).setParseAction( pushFirst ) )
term = Forward()
term = atom + ZeroOrMore(( multop + expr ))
expr << term + ZeroOrMore(( addop + expr ))
