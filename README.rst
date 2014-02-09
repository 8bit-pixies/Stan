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

