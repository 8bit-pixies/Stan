# sas parse.py

from data_lex import dataStepStmt

def id_convert(v_ls, data):
    # this statement needs to have testing
    # refer to stanexpr.ID_ to see how identifiers are parsed
    var_stmt = []
    for el in v_ls:
        try:            
            var_stmt.append("%s%s" % (data, el.id)) #if the expr is an identifier
        except:
            var_stmt.append(el)
    return ''.join(var_stmt)

def logic_convert(v_ls, data):
    # this statement will need testing
    # this will be a recursive call

    # "neg" if b < 0 else "pos" if b > 0 else "zero"
    if 'l_result' in v_ls.keys() and 'l_cond' in v_ls.keys():
        lmd = '%s ' % id_convert(v_ls.l_result, 'x')
        lmd += 'if %s ' % id_convert(v_ls.l_cond, 'x')
        # print "r_cond: ", logic_convert(v_ls.r_cond, 'x')
        lmd += 'else %s ' % id_convert(logic_convert(v_ls.r_cond, 'x'), 'x')
    else:
        lmd = id_convert(v_ls, 'x')
    return lmd

def stan(cstr):
    inf = dataStepStmt.parseString(cstr)
    bd = inf.asDict()
    
    ss = ''
    ss = bd['set']['name'][0]
    data = bd['data']['name'][0]
    
    # looking through set options
    if len(bd['set'].keys()) == 0: 
        pass
    else: 
        # check all the keys...
        for key in bd['set'].keys():
            if key == 'rename':
                #print bd['set']['rename']
                rename_ls = ",".join(["'%s':'%s'" % (x,y) for x,y in bd['set']['rename']])
                ss += '.rename(columns={%s})' % (rename_ls)
            if key == 'drop':
                drop_ls = ",".join(["'%s'" % x for x in bd['set']['drop']])
                ss += '.drop([%s],1)' % drop_ls
        ss = "%s=%s\n" % (data, ss)
    
    # check logic_stmt
    
    if 'stmt' in bd.keys():
        for stmt in bd['stmt']:
            if 'logical' in stmt.keys():
                # the lambda function for the logical statement
                # if elif else pattern for lambda 
                # a = "neg" if b<0 else "pos" if b>0 else "zero"
                lmd = logic_convert(stmt.logical, data)
                ss += "%s['%s']=%s.apply(lambda x : %s, axis=1)\n" % (data, stmt[0], data, lmd)
            elif 'fcall' in stmt.keys():
                # you need to have a apply 
                # probably a way to do it using pandas.DataFrame.apply though
                # the syntax may be harder to parse
                var_stmt = id_convert(stmt[1:], 'x')
                ss += "%s['%s']=%s.apply(lambda x: %s, axis=1)\n" % (data, stmt[0], data, var_stmt)
            else:
                # print stmt
                var_stmt = id_convert(stmt[1:], data)
                ss += "%s['%s']=%s\n" % (data, stmt[0], var_stmt)
    
    # check data options
    if len(bd['data'].keys()) == 0: 
        pass
    else: 
        # check all the keys...
        datas = data
        for key in bd['data'].keys():
            if key == 'rename':
                #print bd['data']['rename']
                rename_ls = ",".join(["'%s':'%s'" % (x,y) for x,y in bd['data']['rename']])
                datas += '.rename(columns={%s})' % (rename_ls)
            if key == 'drop':
                drop_ls = ",".join(["'%s'" % x for x in bd['data']['drop']])
                datas += '.drop([%s],1)' % drop_ls
        ss += "%s=%s\n" % (data, datas)

    return ss

