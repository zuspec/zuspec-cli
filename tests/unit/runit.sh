#!/bin/sh

tests_unit_dir=$(dirname $(realpath $0))
zuspec_dir=$(dirname $(dirname $tests_unit_dir))
echo "tests_unit_dir: $tests_unit_dir $zuspec_dir"

export PYTHONPATH=${zuspec_dir}/src:${zuspec_dir}/tests

#GDB="gdb --args "
#VALGRIND="valgrind --tool=memcheck "

$GDB $VALGRIND ${zuspec_dir}/packages/python/bin/python -m unittest unit.test_py_user_api.TestPyUserApi.test_dotgen

