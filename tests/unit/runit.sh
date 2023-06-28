#!/bin/sh

tests_unit_dir=$(dirname $(realpath $0))
zuspec_dir=$(dirname $(dirname $tests_unit_dir))
echo "tests_unit_dir: $tests_unit_dir $zuspec_dir"

export PYTHONPATH=${zuspec_dir}/src:${zuspec_dir}/tests

#GDB="gdb --args "
#VALGRIND="valgrind --tool=memcheck "
#export PYTHONMALLOC=malloc

$GDB $VALGRIND ${zuspec_dir}/packages/python/bin/python -m unittest unit.test_model_eval.TestModelEval.test_runner_basics

