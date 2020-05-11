# VendingSalesReportingPython

# Dependencies

sudo pip3 install --upgrade pip

## yaml

pip install pyyaml

## Postgres

pip install psycopg2


  In file included from psycopg/psycopgmodule.c:28:0:
    ./psycopg/psycopg.h:35:20: fatal error: Python.h: No such file or directory
     #include <Python.h>
                        ^
    compilation terminated.


# Centos 7
scl enable rh-python36 bash
unset LD_LIBRARY_PATH
pip install --user --upgrade pip
jjs ~/python_projects/pdssr>python -m pip install psycopg2
Defaulting to user installation because normal site-packages is not writeable
Requirement already satisfied: psycopg2 in /opt/rh/rh-python36/root/usr/lib64/python3.6/site-packages (2.8.2)
Could not build wheels for psycopg2, since package 'wheel' is not installed.




# Postgres

Setup the database 

## Install postgres

## Create sales_r

# Requirements


* xlsxwriter
* Sphinx
* json-rpc
* pyusps
* urllib2
* yaml
* psycopg2
* python-ach


# VendingSalesReportingPython

# Dependencies

sudo pip3 install --upgrade pip

## yaml

pip install pyyaml

## Postgres

pip install psycopg2


  In file included from psycopg/psycopgmodule.c:28:0:
    ./psycopg/psycopg.h:35:20: fatal error: Python.h: No such file or directory
     #include <Python.h>
                        ^
    compilation terminated.


# Centos 7
scl enable rh-python36 bash
unset LD_LIBRARY_PATH
pip install --user --upgrade pip


jjs ~/python_projects/pdssr>python -m pip install psycopg2
Defaulting to user installation because normal site-packages is not writeable
Requirement already satisfied: psycopg2 in /opt/rh/rh-python36/root/usr/lib64/python3.6/site-packages (2.8.2)
Could not build wheels for psycopg2, since package 'wheel' is not installed.

# tests/integration_test


# Postgres

Setup the database 


# TODO

externalize dbname from tests/integration_tests


Run test

python pdssr/setup.py test

currently fails as ut_condition_row_msg does not exist

it is declared in pdssr/config/ut_condition_tables and in pdsutil/resourc3s/k

