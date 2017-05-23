@echo off
rem Batch script for running the test suite.
rem Requires the python package `nose` to be installed.
set nosetests=call python -W ignore::DeprecationWarning -m nose

%nosetests% ^
tests/test_provided_code.py ^
tests/test_1_parsing.py ^
tests/test_2_evaluating_simple_expressions.py ^
tests/test_3_evaluating_complex_expressions.py ^
tests/test_4_working_with_variables_and_environments.py ^
tests/test_5_adding_functions_to_the_mix.py ^
tests/test_6_working_with_lists.py ^
tests/test_7_using_the_language.py ^
tests/test_8_final_touches.py ^
tests/test_sanity_checks.py ^
--stop
