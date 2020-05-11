set -x
export PYTHONPATH=`pwd`
scl enable rh-python36 bash
unset LD_LIBARY_PATH
python pdssr/setup.py test

#iython pdssr/tests/integration_test.py


