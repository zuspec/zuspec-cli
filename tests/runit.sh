#!/bin/sh

tests_dir=$(dirname $(realpath $0))
proj_dir=$(dirname $tests_dir)

export PYTHONPATH=$proj_dir/src:${tests_dir}

gdb --args $proj_dir/packages/python/bin/python -m unittest unit.test_reg_model.TestRegModel.test_read32
