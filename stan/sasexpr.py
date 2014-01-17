from pyparsing import *

exprStack = []

def pushFirst( strg, loc, toks ):
    exprStack.append( toks[0] )

def pushUMinus( strg, loc, toks ):
    if toks and toks[0]=='-': 
        exprStack.append( 'unary -' )
        #~ exprStack.append( '-1' )
        #~ exprStack.append( '*' )

point = Literal( "." )
fnumber = Combine(Word(nums) + Optional( point + Optional( Word(nums))))
 
ID_ = Word(alphas+'_', alphanums)
 
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
atom = ( pi | fnumber | ID_ | (lpar + expr +rpar)) # deal with `a = -1` later

# by defining exponentiation as "atom [ ^ factor ]..." instead of "atom [ ^ atom ]...", we get right-to-left exponents, instead of left-to-righ
# that is, 2^3^2 = 2^(3^2), not (2^3)^2.
#factor = Forward()
#factor << atom + ZeroOrMore( ( expop + factor ).setParseAction( pushFirst ) )
term = Forward()
term = atom + ZeroOrMore(( multop + expr ))
expr << term + ZeroOrMore(( addop + expr ))
