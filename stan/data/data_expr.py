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

mod = Keyword("%")

ge = Keyword(">=")
gt = Keyword(">")
le = Keyword("<")
lt = Keyword("<=")
eq = Keyword("=") # change this otherwise statements like a = b = c can be confusing, since it would be a = (b == c)

lpar  = Literal( "(" )
rpar  = Literal( ")" )
addop  = plus | minus
multop = mult | div
otherop = mod
logic = ge | gt | le | lt | eq
pi    = CaselessLiteral( "_PI_" )

EXPR_ = Forward()
FCALL_ = ID_ + "(" + Optional(EXPR_ + ZeroOrMore( "," + EXPR_ )) + ")"
atom = (FCALL_.setResultsName('fcall') | pi | NUM_ | STR_ | Group(ID_.setResultsName('id')) | (lpar + EXPR_ +rpar))

term = Forward()
term = atom + ZeroOrMore(( multop + EXPR_ ))
EXPR_ << term + ZeroOrMore(( addop + EXPR_ )) + ZeroOrMore(( otherop + EXPR_ ))
#

# the logical statement may need to be changed in the future to support the way sas handles it, particularly the "if then do end" pattern
# SAS Logical specific expressions

SEXPR_ = EXPR_ + ZeroOrMore(( logic + EXPR_ ))

DOEXPR = (ID_ + Suppress("=") + EXPR_ + SEMI_).setResultsName('singleExpr') | (Suppress(DO) + SEMI_ + OneOrMore(Group(ID_ + Suppress("=") + EXPR_) + SEMI_) + Suppress(END) + SEMI_)

SASLOGICAL_ = Forward()
SASLOGICAL_ << IF + Group(SEXPR_).setResultsName('l_cond') + THEN + Group(DOEXPR).setResultsName('assign')  + Group(Optional(ELSE.suppress() + (SASLOGICAL_ | Group(DOEXPR).setResultsName('assign')))).setResultsName('r_cond')

ss = """if a = 1 then a = 2+2;"""
sd = """if a = 1 then do;
    b = 1;
    c = 2;
    """

def id_convert(v_ls, data, cond = ''):
    """id convert changes variable ids to the Pandas format. Returns a converted string
    
    It iterates through list of tokens checking whether it is a reserved keyword
    or not.
    
    Parameters
    ----------
    
    v_ls : list of tokens
    data : the source Pandas DataFrame
    
    """
    var_stmt = []
    for el in v_ls:
        try: 
            if el.id not in RESERVED_KEYWORDS:
                if cond != '':
                    var_stmt.append("%s.ix[(%s),'%s']" % (data, cond, el.id[0])) #if the expr is an identifier
                else:
                    var_stmt.append("%s%s" % (data, el.id)) #if the expr is an identifier
            else:
                var_stmt.append(el)
        except:
            if el == '=' : el = '=='
            var_stmt.append(el)
    return ''.join(var_stmt)

import pandas as pd
import numpy as np
data = 'df'

df = pd.DataFrame(np.arange(1,26).reshape(5,5), columns = list('abcde'))  
df_a = np.where(df['a'] % 2 == 0)[0]

sd = """if (a % 2) = 0 then 
a = a+1; else b = a;
"""

sd1 = """if (a % 2) = 0 then do; 
a = a+1; b= c+1;

end;
else do;
a = a-1;
b = b-1;
end;
"""

sd2 = """if (a % 2) = 0 then do; 
a = a+1; b= c+1;

end;
else if (a % 3) = 0 then c = 2;
else do;
a = a-1;
b = b-1;
end;
"""

a = SASLOGICAL_.parseString(sd).asDict()
ss = ''

def _logic(v_ls, data, cond_list = []):
    ss = ''
    for el in v_ls:
        if el == 'l_cond':
            # df.ix[(df['a']%2 ==0), 'a'] = df[(df['a']%2 ==0)]['a'] + 1 
            cond = id_convert(v_ls['l_cond'], data)
            cond_list.append(cond)
            cond_list = list(set(cond_list))
        elif el == 'assign':
            cond_ = " and ".join(["not(%s)" % x for x in cond_list if x != cond and x != '']+[cond])
            if 'singleExpr' in v_ls['assign'].keys():
                stmt = v_ls['assign']                  
                var_stmt = id_convert(stmt[1:], data, cond=cond_)
                ss += "%s.ix[(%s), '%s'] = %s\n" % (data, cond_, stmt[0], var_stmt)
                #ss = "    %s.loc[i,'%s']=%s\n" % (data, stmt[0], var_stmt)
            else:
                for stmt in v_ls['assign']:
                    var_stmt = id_convert(stmt[1:], data, cond = cond_)
                    ss += "%s.ix[(%s), '%s'] = %s\n" % (data, cond_, stmt[0], var_stmt)
        
    if 'r_cond' in v_ls.keys() and len(v_ls['r_cond']) != 0:
        cond_ = " and ".join(["not(%s)" % x for x in cond_list])
        if 'l_cond' in v_ls['r_cond'].keys():
            ss += _logic(v_ls['r_cond'], data, cond_list)
            print "note:", _logic(v_ls['r_cond'], data, cond_list)
            print "l_cond:", v_ls['r_cond']['l_cond']
            print "\n---\n"
        elif 'assign' in v_ls['r_cond'].keys():
            if 'singleExpr' in v_ls['r_cond']['assign'].keys():
                stmt = v_ls['r_cond']['assign']                  
                var_stmt = id_convert(stmt[1:], data, cond=cond_)
                ss += "%s.ix[(%s), '%s'] = %s\n" % (data, cond_, stmt[0], var_stmt)
                #ss = "    %s.loc[i,'%s']=%s\n" % (data, stmt[0], var_stmt)
            else:
                for stmt in v_ls['r_cond']['assign']:
                    var_stmt = id_convert(stmt[1:], data, cond = cond_)
                    ss += "%s.ix[(%s), '%s'] = %s\n" % (data, cond_, stmt[0], var_stmt)
        
        else:
            if 'singleExpr' in v_ls['r_cond'].keys():
                var_stmt = id_convert(v_ls['r_cond'][1:], data, cond=cond_)
                ss += "%s.ix[(%s), '%s'] = %s\n" % (data, cond_, v_ls['r_cond'][0], var_stmt)
                
    return ss

cc = _logic(a, data)
cc1 = _logic(SASLOGICAL_.parseString(sd1).asDict(), data)
cc2 = _logic(SASLOGICAL_.parseString(sd2).asDict(), data)
bb2 = SASLOGICAL_.parseString(sd2).asDict()