"""
The :mod:`stan.proc.proc_expr` module is the parser for SAS-like language.
"""

from pyparsing import *
import functools

RESERVED_KEYWORDS = "data proc rename run drop keep".split()
SEMI_ = Suppress(";")

# define SAS reserved words
DATA, PROC, RENAME, RUN, DROP, KEEP = map(functools.partial(Keyword, caseless=True),
                                    RESERVED_KEYWORDS)

ID_ = Word(alphas+"_", alphanums+"_")

STR_ = (QuotedString(quoteChar="'", escChar='\\', multiline=True, unquoteResults=True) | 
        QuotedString(quoteChar='"', escChar='\\', multiline=True, unquoteResults=True)).setResultsName('str_type') # since there is no string manipulation we should unquote the result

NUM_ = Combine(Optional("-") + Word(nums) + Optional( Literal( "." ) + Optional( Word(nums)))).setResultsName('num_type')

PROC_ = Forward()

PROC_ << (Suppress(PROC) + ID_.setResultsName('func') + ZeroOrMore(Group(ID_ + ((Suppress("=") + (STR_ | NUM_ | ID_)) | OneOrMore(STR_ | NUM_ | ID_))))  + SEMI_ + 
          ZeroOrMore(Group(ID_ + ((Suppress("=") + (STR_ | NUM_ | ID_)) | OneOrMore(STR_ | NUM_ | ID_))) + SEMI_) +
          Suppress(RUN) + SEMI_) # this needs to be generic enough to handle unseen IDs before

