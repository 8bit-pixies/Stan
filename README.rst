Statistical Analysis System (SAS) Transcompiler to SciPy
==================================================

.. image:: https://travis-ci.org/chappers/Stan.png?branch=dev   :target: https://travis-ci.org/chappers/Stan

The goal of this is to transcompile a subset of SAS/Base to SciPy.

Testing
-------

The tests can be run directly inside your git clone (without having to install stan) by typing:

    nosetests stan


Differences
-----------

* ``data merge`` will not require the data to be sorted before hand. Data will be implicitly sorted
  (similar to the SPDE engine).
* ``dates`` will be suppported in a different manner (coming soon).
* ``format``, ``length``, ``informats`` will not be necessary (we shall use ``dtype`` in ``numpy``).
* Pandas supports column names with spaces in it. This may cause issues since SAS automatically changes spaces to ``_``. 
* Pandas is case sensitive, SAS is not.

Known Issues
------------

Will not Suport
---------------

* ``macro`` facility. It can be replicated (to a degree) using `iPython <http://ipython.org/ipython-doc/rel-1.1.0/interactive/reference.html#input-caching-system>`_.


Example
-------


.. code:: python

    from stan.transcompile import transcompile
    import stan.stan_magic
    from pandas import DataFrame
    import numpy as np
    import pkgutil
    from numpy import nan
.. code:: python

    import stan.proc_functions as proc_func
    
    mod_name = ["from stan.proc_functions import %s" % name for _, name, _ in pkgutil.iter_modules(proc_func.__path__)] 
    exec("\n".join(mod_name))
.. code:: python

    # create an example data frame 
    df = DataFrame(np.random.randn(10, 5), columns = ['a','b','c','d','e'])
    df



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>a</th>
          <th>b</th>
          <th>c</th>
          <th>d</th>
          <th>e</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>-1.245481</td>
          <td>-1.609963</td>
          <td> 0.442550</td>
          <td>-0.056406</td>
          <td>-0.213349</td>
        </tr>
        <tr>
          <th>1</th>
          <td>-1.118754</td>
          <td> 0.116146</td>
          <td>-0.032579</td>
          <td>-0.556940</td>
          <td> 0.270678</td>
        </tr>
        <tr>
          <th>2</th>
          <td> 0.864960</td>
          <td>-0.479118</td>
          <td> 2.370390</td>
          <td> 2.090656</td>
          <td>-0.475426</td>
        </tr>
        <tr>
          <th>3</th>
          <td> 0.434934</td>
          <td>-2.510176</td>
          <td> 0.122871</td>
          <td> 0.077915</td>
          <td> 0.597477</td>
        </tr>
        <tr>
          <th>4</th>
          <td> 0.689308</td>
          <td> 0.042817</td>
          <td> 0.217040</td>
          <td>-1.424120</td>
          <td>-0.214721</td>
        </tr>
        <tr>
          <th>5</th>
          <td>-0.432170</td>
          <td>-1.344882</td>
          <td>-0.055934</td>
          <td> 1.921247</td>
          <td> 1.519922</td>
        </tr>
        <tr>
          <th>6</th>
          <td>-0.837277</td>
          <td> 0.944802</td>
          <td>-0.650114</td>
          <td>-0.297314</td>
          <td> 1.432118</td>
        </tr>
        <tr>
          <th>7</th>
          <td> 1.488292</td>
          <td>-1.236296</td>
          <td> 0.128023</td>
          <td> 2.886408</td>
          <td>-0.560200</td>
        </tr>
        <tr>
          <th>8</th>
          <td>-0.510566</td>
          <td>-1.736577</td>
          <td> 0.066769</td>
          <td>-0.735257</td>
          <td> 0.178167</td>
        </tr>
        <tr>
          <th>9</th>
          <td> 2.540022</td>
          <td> 0.034493</td>
          <td>-0.521496</td>
          <td>-2.189938</td>
          <td> 0.111702</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    %%stan
    data test;
    set df (drop = a);
    run;



.. parsed-literal::

    u"test=df.drop(['a'],1)\n"



.. code:: python

    exec(_)
    test



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>b</th>
          <th>c</th>
          <th>d</th>
          <th>e</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>-1.609963</td>
          <td> 0.442550</td>
          <td>-0.056406</td>
          <td>-0.213349</td>
        </tr>
        <tr>
          <th>1</th>
          <td> 0.116146</td>
          <td>-0.032579</td>
          <td>-0.556940</td>
          <td> 0.270678</td>
        </tr>
        <tr>
          <th>2</th>
          <td>-0.479118</td>
          <td> 2.370390</td>
          <td> 2.090656</td>
          <td>-0.475426</td>
        </tr>
        <tr>
          <th>3</th>
          <td>-2.510176</td>
          <td> 0.122871</td>
          <td> 0.077915</td>
          <td> 0.597477</td>
        </tr>
        <tr>
          <th>4</th>
          <td> 0.042817</td>
          <td> 0.217040</td>
          <td>-1.424120</td>
          <td>-0.214721</td>
        </tr>
        <tr>
          <th>5</th>
          <td>-1.344882</td>
          <td>-0.055934</td>
          <td> 1.921247</td>
          <td> 1.519922</td>
        </tr>
        <tr>
          <th>6</th>
          <td> 0.944802</td>
          <td>-0.650114</td>
          <td>-0.297314</td>
          <td> 1.432118</td>
        </tr>
        <tr>
          <th>7</th>
          <td>-1.236296</td>
          <td> 0.128023</td>
          <td> 2.886408</td>
          <td>-0.560200</td>
        </tr>
        <tr>
          <th>8</th>
          <td>-1.736577</td>
          <td> 0.066769</td>
          <td>-0.735257</td>
          <td> 0.178167</td>
        </tr>
        <tr>
          <th>9</th>
          <td> 0.034493</td>
          <td>-0.521496</td>
          <td>-2.189938</td>
          <td> 0.111702</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    %%stan
    data df_if;
        set df;    
        if b < 0.3 then x = 0;
        else if b < 0.6 then x = 1;
        else x = 2;    
    run;



.. parsed-literal::

    u"df_if=df\nfor el in ['x']:\n    if el not in df_if.columns:\n        df_if[el] = np.nan\ndf_if.ix[((df_if[u'b']<0.3)), 'x'] = (0)\nfor el in ['x']:\n    if el not in df_if.columns:\n        df_if[el] = np.nan\ndf_if.ix[((~((df_if[u'b']<0.3))) & (df_if[u'b']<0.6)), 'x'] = (1)\ndf_if.ix[((~((df_if[u'b']<0.6))) & (~((df_if[u'b']<0.3)))), 'x'] = (2)\n"



.. code:: python

    exec(_)
    df_if



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>a</th>
          <th>b</th>
          <th>c</th>
          <th>d</th>
          <th>e</th>
          <th>x</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>-1.245481</td>
          <td>-1.609963</td>
          <td> 0.442550</td>
          <td>-0.056406</td>
          <td>-0.213349</td>
          <td> 0</td>
        </tr>
        <tr>
          <th>1</th>
          <td>-1.118754</td>
          <td> 0.116146</td>
          <td>-0.032579</td>
          <td>-0.556940</td>
          <td> 0.270678</td>
          <td> 0</td>
        </tr>
        <tr>
          <th>2</th>
          <td> 0.864960</td>
          <td>-0.479118</td>
          <td> 2.370390</td>
          <td> 2.090656</td>
          <td>-0.475426</td>
          <td> 0</td>
        </tr>
        <tr>
          <th>3</th>
          <td> 0.434934</td>
          <td>-2.510176</td>
          <td> 0.122871</td>
          <td> 0.077915</td>
          <td> 0.597477</td>
          <td> 0</td>
        </tr>
        <tr>
          <th>4</th>
          <td> 0.689308</td>
          <td> 0.042817</td>
          <td> 0.217040</td>
          <td>-1.424120</td>
          <td>-0.214721</td>
          <td> 0</td>
        </tr>
        <tr>
          <th>5</th>
          <td>-0.432170</td>
          <td>-1.344882</td>
          <td>-0.055934</td>
          <td> 1.921247</td>
          <td> 1.519922</td>
          <td> 0</td>
        </tr>
        <tr>
          <th>6</th>
          <td>-0.837277</td>
          <td> 0.944802</td>
          <td>-0.650114</td>
          <td>-0.297314</td>
          <td> 1.432118</td>
          <td> 2</td>
        </tr>
        <tr>
          <th>7</th>
          <td> 1.488292</td>
          <td>-1.236296</td>
          <td> 0.128023</td>
          <td> 2.886408</td>
          <td>-0.560200</td>
          <td> 0</td>
        </tr>
        <tr>
          <th>8</th>
          <td>-0.510566</td>
          <td>-1.736577</td>
          <td> 0.066769</td>
          <td>-0.735257</td>
          <td> 0.178167</td>
          <td> 0</td>
        </tr>
        <tr>
          <th>9</th>
          <td> 2.540022</td>
          <td> 0.034493</td>
          <td>-0.521496</td>
          <td>-2.189938</td>
          <td> 0.111702</td>
          <td> 0</td>
        </tr>
      </tbody>
    </table>
    </div>



--------------




.. code:: python

    # procs can be added manually they can be thought of as python functions
    # you can define your own, though I need to work on the parser
    # to get it "smooth"
    
    df1 = DataFrame({'a' : [1, 0, 1], 'b' : [0, 1, 1] }, dtype=bool)
    df1



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>a</th>
          <th>b</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>  True</td>
          <td> False</td>
        </tr>
        <tr>
          <th>1</th>
          <td> False</td>
          <td>  True</td>
        </tr>
        <tr>
          <th>2</th>
          <td>  True</td>
          <td>  True</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    %%stan
    proc describe data = df1 out = df2;
    by a;
    run;



.. parsed-literal::

    u"df2=describe.describe(data=df1,by='a')"



.. code:: python

    exec(_)
    df2



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>a</th>
          <th>b</th>
        </tr>
        <tr>
          <th>a</th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="8" valign="top">False</th>
          <th>count</th>
          <td>     1</td>
          <td>         1</td>
        </tr>
        <tr>
          <th>mean</th>
          <td>     0</td>
          <td>         1</td>
        </tr>
        <tr>
          <th>std</th>
          <td>   NaN</td>
          <td>       NaN</td>
        </tr>
        <tr>
          <th>min</th>
          <td> False</td>
          <td>      True</td>
        </tr>
        <tr>
          <th>25%</th>
          <td> False</td>
          <td>      True</td>
        </tr>
        <tr>
          <th>50%</th>
          <td>     0</td>
          <td>         1</td>
        </tr>
        <tr>
          <th>75%</th>
          <td> False</td>
          <td>      True</td>
        </tr>
        <tr>
          <th>max</th>
          <td> False</td>
          <td>      True</td>
        </tr>
        <tr>
          <th rowspan="8" valign="top">True </th>
          <th>count</th>
          <td>     2</td>
          <td>         2</td>
        </tr>
        <tr>
          <th>mean</th>
          <td>     1</td>
          <td>       0.5</td>
        </tr>
        <tr>
          <th>std</th>
          <td>     0</td>
          <td> 0.7071068</td>
        </tr>
        <tr>
          <th>min</th>
          <td>  True</td>
          <td>     False</td>
        </tr>
        <tr>
          <th>25%</th>
          <td>     1</td>
          <td>      0.25</td>
        </tr>
        <tr>
          <th>50%</th>
          <td>     1</td>
          <td>       0.5</td>
        </tr>
        <tr>
          <th>75%</th>
          <td>     1</td>
          <td>      0.75</td>
        </tr>
        <tr>
          <th>max</th>
          <td>  True</td>
          <td>      True</td>
        </tr>
      </tbody>
    </table>
    </div>



The proc actually isn't difficult to write. So for the above code it is

actually just this:



::



    def describe(data, by):

        return data.groupby(by).describe()  



This functionality allow you to handle most of the ``by`` and ``retain``

cases. For languages like Python and R, the normal way to handle data is

through the split-apply-combine methodology.



Merges can be achieved in a similar way, by creating a ``proc``:


.. code:: python

    %%stan
    proc merge out = df2;
    dt_left left;
    dt_right right;
    on = 'key';
    run;



.. parsed-literal::

    u"df2=merge.merge(dt_left=left,dt_right=right,on='key')"



.. code:: python

    left = DataFrame({'key': ['foo', 'foo'], 'lval': [1, 2]})
    right = DataFrame({'key': ['foo', 'foo'], 'rval': [4, 5]})
    
    exec(_)
    df2



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>key</th>
          <th>lval</th>
          <th>rval</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td> foo</td>
          <td> 1</td>
          <td> 4</td>
        </tr>
        <tr>
          <th>1</th>
          <td> foo</td>
          <td> 1</td>
          <td> 5</td>
        </tr>
        <tr>
          <th>2</th>
          <td> foo</td>
          <td> 2</td>
          <td> 4</td>
        </tr>
        <tr>
          <th>3</th>
          <td> foo</td>
          <td> 2</td>
          <td> 5</td>
        </tr>
      </tbody>
    </table>
    </div>



heres an example showing how you can define your own function and run it

(not a function that came with the package)


.. code:: python

    def sum_mean_by(data, by):
        return data.groupby(by).agg([np.sum, np.mean]) 
.. code:: python

    %%stan
    proc sum_mean_by data = df_if out = df_sum;
    by x;
    run;



.. parsed-literal::

    u"df_sum=sum_mean_by(data=df_if,by='x')"



.. code:: python

    exec(_)
    df_sum



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr>
          <th></th>
          <th colspan="2" halign="left">a</th>
          <th colspan="2" halign="left">b</th>
          <th colspan="2" halign="left">c</th>
          <th colspan="2" halign="left">d</th>
          <th colspan="2" halign="left">e</th>
        </tr>
        <tr>
          <th></th>
          <th>sum</th>
          <th>mean</th>
          <th>sum</th>
          <th>mean</th>
          <th>sum</th>
          <th>mean</th>
          <th>sum</th>
          <th>mean</th>
          <th>sum</th>
          <th>mean</th>
        </tr>
        <tr>
          <th>x</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td> 2.710545</td>
          <td> 0.301172</td>
          <td>-8.723557</td>
          <td>-0.969284</td>
          <td> 2.737635</td>
          <td> 0.304182</td>
          <td> 2.013566</td>
          <td> 0.223730</td>
          <td> 1.214251</td>
          <td> 0.134917</td>
        </tr>
        <tr>
          <th>2</th>
          <td>-0.837277</td>
          <td>-0.837277</td>
          <td> 0.944802</td>
          <td> 0.944802</td>
          <td>-0.650114</td>
          <td>-0.650114</td>
          <td>-0.297314</td>
          <td>-0.297314</td>
          <td> 1.432118</td>
          <td> 1.432118</td>
        </tr>
      </tbody>
    </table>
    </div>



``proc sql`` is supported through the ``pandasql`` library. So the above

table could have been produced via SQL as well.


.. code:: python

    import pandasql
    
    q = """
    select 
        sum(a) as sum_a,
        sum(b) as sum_b,
        sum(c) as sum_c,
        sum(d) as sum_d,
        sum(e) as sum_e,
        avg(a) as avg_a,
        avg(b) as avg_b,
        avg(c) as avg_c,
        avg(d) as avg_d,
        avg(e) as avg_e
    from
        df_if
    group by x
    """
    
    df_sum_sql = pandasql.sqldf(q, locals())
    df_sum_sql
    
    



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>sum_a</th>
          <th>sum_b</th>
          <th>sum_c</th>
          <th>sum_d</th>
          <th>sum_e</th>
          <th>avg_a</th>
          <th>avg_b</th>
          <th>avg_c</th>
          <th>avg_d</th>
          <th>avg_e</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td> 2.710545</td>
          <td>-8.723557</td>
          <td> 2.737635</td>
          <td> 2.013566</td>
          <td> 1.214251</td>
          <td> 0.301172</td>
          <td>-0.969284</td>
          <td> 0.304182</td>
          <td> 0.223730</td>
          <td> 0.134917</td>
        </tr>
        <tr>
          <th>1</th>
          <td>-0.837277</td>
          <td> 0.944802</td>
          <td>-0.650114</td>
          <td>-0.297314</td>
          <td> 1.432118</td>
          <td>-0.837277</td>
          <td> 0.944802</td>
          <td>-0.650114</td>
          <td>-0.297314</td>
          <td> 1.432118</td>
        </tr>
      </tbody>
    </table>
    </div>


