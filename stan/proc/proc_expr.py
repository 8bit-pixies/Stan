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

PROC_ = Forward()

PROC_ << (Suppress(PROC) + ID_.setResultsName('func') + Group(ZeroOrMore(ID_ + Optional(Suppress("=")) + OneOrMore(ID_))) + SEMI_ + 
          Group(ZeroOrMore(ID_ + Optional(Suppress("=")) + OneOrMore(ID_))) + SEMI_ +
          Suppress(RUN) + SEMI_) # this needs to be generic enough to handle unseen IDs before

