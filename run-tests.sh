#!/usr/bin/env bash

# Bash script for running the test suite every time a file is changed.
# Requires the python package `nose` to be installed, as well as the
# `inotifytools` commands.

while inotifywait -r -e modify . ; do
    nosetests --stop
    # nosetests tests/test_2_evaluating_simple_expressions.py --stop
#    nosetests tests/test_provided_parsing.py --stop
#    nosetests tests/test_1_parsing.py --stop
done
