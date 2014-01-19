from pyparsing import *
from stanlexer_fcall import function_call as FUNC_

exprStack = []

point = Literal( "." )
fnumber = Combine(Word(nums) + Optional( point + Optional( Word(nums))))
 
ID_ = Word(alphas+"_", alphanums+"_")
STR_ = quotedString.addParseAction(removeQuotes)\

# Operators
 
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
atom = ( FUNC_ | pi | fnumber | ID_ | STR_ | (lpar + expr +rpar)) # deal with `a = -1` later

# by defining exponentiation as "atom [ ^ factor ]..." instead of "atom [ ^ atom ]...", we get right-to-left exponents, instead of left-to-righ
# that is, 2^3^2 = 2^(3^2), not (2^3)^2.
#factor = Forward()
#factor << atom + ZeroOrMore( ( expop + factor ).setParseAction( pushFirst ) )

# ensure precedence is kept
term = Forward()
term = atom + ZeroOrMore(( multop + expr ))
expr << (term + ZeroOrMore(( addop + expr )))

#def test(s):
#    print s, "->"
#    print expr.parseString(s)
#    # insert stuff...

#expr.validate()
#test("1+2")
#test("a+b+2")
#test('"Chapman"')
#test('substr(Name,1,1)')
#test('( a + b)')