"""
The :mod:`stan.data.data_parse` module is the data step parser for SAS-like language.
"""

from stan.data.data_lex import dataStepStmt
from stan.data.data_expr import RESERVED_KEYWORDS

def _id_convert(v_ls, data):
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
                var_stmt.append("%s%s" % (data, el.id)) #if the expr is an identifier
            else:
                var_stmt.append(el)
        except:
            var_stmt.append(el)
    return ''.join(var_stmt)

def _set_convert(v_ls, data):
    """set convert converts the set options to Pandas format. Returns a converted string.
        
    Parameters
    ----------
    
    v_ls : list of tokens
    data : the source Pandas DataFrame
    
    """
    # check all the keys...
    ss = v_ls['name'][0]
    for key in v_ls.keys():
        if key == 'rename':
            rename_ls = ",".join(["'%s':'%s'" % (x,y) for x,y in v_ls['rename']])
            ss += '.rename(columns={%s})' % (rename_ls)
        if key == 'drop':
            drop_ls = ",".join(["'%s'" % x for x in v_ls['drop']])
            ss += '.drop([%s],1)' % drop_ls
    ss = "%s=%s\n" % (data, ss)
    return ss

def _data_convert(v_ls, data):
    """data convert converts the data options to Pandas format. Returns a converted string.
        
    Parameters
    ----------
    
    v_ls : list of tokens
    data : the source Pandas DataFrame
    
    """
    datas = data
    for key in v_ls.keys():
        if key == 'rename':
            rename_ls = ",".join(["'%s':'%s'" % (x,y) for x,y in v_ls['rename']])
            datas += '.rename(columns={%s})' % (rename_ls)
        if key == 'drop':
            drop_ls = ",".join(["'%s'" % x for x in v_ls['drop']])
            datas += '.drop([%s],1)' % drop_ls
    return "%s=%s\n" % (data, datas) if data != datas else ""
           
def data_parse(cstr):
    """data_parse parses the string and returns a Pandas compatible string
    
    Parameters
    ----------
    
    cstr : string written in SAS-like language
    
    """
    inf = dataStepStmt.parseString(cstr)
    bd = inf.asDict()
    
    ss = ''
    data = bd['data']['name'][0]
    
    # looking through set options
    if len(bd['set'].keys()) == 0: 
        pass
    else: 
        set_str = _set_convert(bd['set'], data)
        ss = set_str

    # check logic_stmt    
    if 'stmt' in bd.keys():
        for stmt in bd['stmt']:
            if 'fcall' in stmt.keys():
                var_stmt = _id_convert(stmt[1:], 'x')
                ss += "%s['%s']=%s.apply(lambda x: %s, axis=1)\n" % (data, stmt[0], data, var_stmt)
            else:
                var_stmt = _id_convert(stmt[1:], data)
                ss += "%s['%s']=%s\n" % (data, stmt[0], var_stmt)
                
    if 'saslogical' in bd.keys():
        pass
    
    # check data options
    if len(bd['data'].keys()) == 0: 
        pass
    else: 
        datas = _data_convert(bd['data'], data)
        ss += datas
    return ss


