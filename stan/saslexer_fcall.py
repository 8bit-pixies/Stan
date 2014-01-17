# saslexer_fcall

from pyparsing import *

testData = """
funcName("paramOne", &paramTwo, fTwo(p0, p1), paramFour);
"""

expr = Forward() 
 
LPAR, RPAR, SEMI = map(Suppress, "();")
ID_ = Word(alphas+"_", alphanums+"_")
function_call = Group(ID_.setResultsName("name") + LPAR + Group(Optional(delimitedList(expr))) + RPAR)
integer = Regex(r"-?\d+")
real = Regex(r"-?\d+\.\d*")
 
operand = (function_call | ID_ | real | integer | quotedString )
expop = Literal('^')
signop = oneOf('+ -')
multop = oneOf('* /')
plusop = oneOf('+ -')
factop = Literal('!')
derefop = OneOrMore('*')
addrop = oneOf('&')
 
expr << operatorPrecedence( operand,
    [(derefop, 1, opAssoc.RIGHT),
     (addrop, 1, opAssoc.RIGHT),
     (factop, 1, opAssoc.LEFT),
     (expop, 2, opAssoc.RIGHT),
     (signop, 1, opAssoc.RIGHT),
     (multop, 2, opAssoc.LEFT),
     (plusop, 2, opAssoc.LEFT),]
    )
 


