#!/usr/bin/env bash

# Bash script for running the test suite every time a file is changed.
# Requires the python package `nose` to be installed, as well as the
# `inotifytools` commands.

function run_tests {
    nosetests tests/test_1_parsing.py --stop
    nosetests tests/test_2_evaluating_simple_expressions.py --stop
    nosetests tests/test_3_evaluating_complex_expressions.py --stop
    nosetests tests/test_4_working_with_variables_and_environments.py --stop
    nosetests tests/test_5_adding_functions_to_the_mix.py --stop
    nosetests tests/test_6_working_with_lists.py --stop
    nosetests tests/test_7_final_language.py --stop

    nosetests tests/test_builtins.py --stop
    nosetests tests/test_provided_code.py --stop
}

run_tests
while inotifywait -r -e modify . ; do
    run_tests
done
