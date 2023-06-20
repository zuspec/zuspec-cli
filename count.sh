#!/bin/sh

count=0

this_c=$(cat $(find src -name '*.py') | wc -l)

count=`expr $count + $this_c`

pyvsc_py=$(cat $(find packages/pyvsc-dataclasses/src -name '*.py') | wc -l)
count=`expr $count + $pyvsc_py`
pyarl_py=$(cat $(find packages/zuspec-dataclasses/src -name '*.py') | wc -l)
count=`expr $count + $pyarl_py`

vsc_h=$(cat $(find packages/vsc-dm/src -name '*.h') | wc -l)
vsc_cpp=$(cat $(find packages/vsc-dm/src -name '*.cpp') | wc -l)
vsc_py=$(cat $(find packages/vsc-dm/python -name '*.p*') | wc -l)

count=`expr $count + $vsc_h`
count=`expr $count + $vsc_cpp`
count=`expr $count + $vsc_py`

vsc_solvers_h=$(cat $(find packages/vsc-solvers/src -name '*.h') | wc -l)
vsc_solvers_cpp=$(cat $(find packages/vsc-solvers/src -name '*.cpp') | wc -l)
vsc_solvers_py=$(cat $(find packages/vsc-solvers/python -name '*.p*') | wc -l)

count=`expr $count + $vsc_solvers_h`
count=`expr $count + $vsc_solvers_cpp`
count=`expr $count + $vsc_solvers_py`

zsp_arl_dm_h=$(cat $(find packages/zuspec-arl-dm/src -name '*.h') | wc -l)
zsp_arl_dm_cpp=$(cat $(find packages/zuspec-arl-dm/src -name '*.cpp') | wc -l)
zsp_arl_dm_py=$(cat $(find packages/zuspec-arl-dm/python -name '*.p*') | wc -l)

count=`expr $count + $zsp_arl_dm_h`
count=`expr $count + $zsp_arl_dm_cpp`
count=`expr $count + $zsp_arl_dm_py`

zsp_arl_eval_h=$(cat $(find packages/zuspec-arl-eval/src -name '*.h') | wc -l)
zsp_arl_eval_cpp=$(cat $(find packages/zuspec-arl-eval/src -name '*.cpp') | wc -l)
zsp_arl_eval_py=$(cat $(find packages/zuspec-arl-eval/python -name '*.p*') | wc -l)

count=`expr $count + $zsp_arl_eval_h`
count=`expr $count + $zsp_arl_eval_cpp`
count=`expr $count + $zsp_arl_eval_py`

zsp_be_sw_h=$(cat $(find packages/zuspec-be-sw/src -name '*.h') | wc -l)
zsp_be_sw_cpp=$(cat $(find packages/zuspec-be-sw/src -name '*.cpp') | wc -l)
zsp_be_sw_py=$(cat $(find packages/zuspec-be-sw/python -name '*.p*') | wc -l)

count=`expr $count + $zsp_be_sw_h`
count=`expr $count + $zsp_be_sw_cpp`
count=`expr $count + $zsp_be_sw_py`

zsp_fe_parser_h=$(cat $(find packages/zuspec-fe-parser/src -name '*.h') | wc -l)
zsp_fe_parser_cpp=$(cat $(find packages/zuspec-fe-parser/src -name '*.cpp') | wc -l)
#zsp_fe_parser_py=$(cat $(find packages/zuspec-fe-parser/python -name '*.p*') | wc -l)
zsp_fe_parser_py=0

count=`expr $count + $zsp_fe_parser_h`
count=`expr $count + $zsp_fe_parser_cpp`
count=`expr $count + $zsp_fe_parser_py`

zsp_parser_h=$(cat $(find packages/zuspec-parser/src -name '*.h') | wc -l)
zsp_parser_cpp=$(cat $(find packages/zuspec-parser/src -name '*.cpp') | wc -l)
zsp_parser_py=$(cat $(find packages/zuspec-parser/python -name '*.p*') | wc -l)

count=`expr $count + $zsp_fe_parser_h`
count=`expr $count + $zsp_fe_parser_cpp`
count=`expr $count + $zsp_fe_parser_py`

echo "count: ${count}"

#debug-mgr
#fltools
#pyastbuilder
#pytypeworks

