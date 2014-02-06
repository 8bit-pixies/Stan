"""
The :mod:`stan.proc.proc_sql` module is the proc sql parser only
"""

#import pandasql
import re

def _convert_code(sql):
    """create_table tries to get the table name from the sql code"""
    tb_re = re.compile(r"(create\s+table\s+([_a-zA-Z][_a-zA-Z0-9]*)\s+as)", re.IGNORECASE)
    tb = tb_re.match(sql.strip())
    code = tb_re.sub('', sql.strip())
    try:
        return '''%s=pandasql.sqldf("""%s""", locals())''' % (tb.group(2), code)
    except:
        return 'pandasql.sqldf("""%s""", locals())' % code


def proc_sql(sql):
    """proc sql converts sql statement to pandas code using pandasql library
    
    Parameters
    ----------
    
    sql : proc sql style code
    
    """   
    
    sql_stmts = sql.split(';')[1:-2] # the first el should be proc sql and the last should be quit; or run;
    return '\n'.join([_convert_code(x) for x in sql_stmts])
    