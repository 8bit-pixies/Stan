# saslexer_fcall

from pyparsing import *

point = Literal( "." )
STR_ = (QuotedString(quoteChar="'", escChar='\\', multiline=True, unquoteResults=False) | 
        QuotedString(quoteChar='"', escChar='\\', multiline=True, unquoteResults=False)).setResultsName('str_type')
fnumber = Combine(Word(nums) + Optional( point + Optional( Word(nums)))).setResultsName('num_type')

expr = Forward() 
 
LPAR = "("
RPAR = ")"
ID_ = Word(alphas+"_", alphanums+"_")
function_call = Group(ID_ + LPAR + Group(Optional(delimitedList(expr))) + RPAR)

 
operand = (function_call | Group(ID_).setResultsName('id') | STR_ | fnumber | STR_ )
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
 


