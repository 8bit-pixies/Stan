Statistical Analysis System Transcompiler to SciPy
==================================================

The goal of this is to transcompile a subset of SAS/Base to SciPy.

Feature Set
-----------


Testing
-------

The tests can be run directly inside your git clone (without having to install stan) by typing:

    nosetests stan


Differences
-----------

* `data merge` will not require the data to be sorted before hand. Data will be implicitly sorted
  (similar to the SPDE engine).
* `dates` will be suppported in a different manner (coming soon).
* `format`, `length`, `informats` will not be necessary (we shall use `dtype` in `numpy`).
* Pandas supports column names with spaces in it. This may cause issues since SAS automatically changes spaces to `_`. 
* Pandas is case sensitive, SAS is not.

Known Issues
------------

Will not Suport
---------------

* `macro` facility (nice to have); You could just write pure python code for it? (python functions)

