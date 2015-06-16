#!/usr/bin/env python3
"""
CSSE1001 Semester 1 2015 - Assignment 1 Sample Tests


Save this file in the same folder as the `assign1.py` file which contains your
solution, and the sample `.txt` files provided.

This program will run a sample of automated test cases on your code, and
check if it runs correctly.

These test cases are not comprehensive - this program will not pick up on every
error in your solution, so you should run your code yourself to check it is
correct. The tutors will run a more complete set of test cases similar to this
when marking your assignment, and you will be able to receive feedback on how
your program performed.

You are not expected to understand how this test program works, but some
students may like to read or modify it.

"""

import traceback
import sys
import os
import functools
import io
import datetime
import pprint

import assign1

STATIONS = ['Carnarvon', 'Perth']

DATES = ['20141219', '20141220', '20141221', '20141222', '20141223', 
         '20141224', '20141225', '20141226', '20141227', '20141228', 
         '20141229', '20141230', '20141231']

PERTH_DATA = [39.2, 28.7, 29.6, 30.0, 32.1, 32.6, 31.9, 33.4, 35.0, 
              31.3, 35.7, 41.5, 29.6]

ALL_DATA = [[28.1, 26.9, 33.6, 36.7, 30.5, 28.9, 34.3, 40.9, 
             41.4, 41.5, 32.3, 30.4, 29.0], 
            [39.2, 28.7, 29.6, 30.0, 32.1, 32.6, 31.9, 33.4, 
             35.0, 31.3, 35.7, 41.5, 29.6]]

DIFF_DATA = [('20141220', 1.8000000000000007), 
             ('20141221', -4.0), 
             ('20141222', -6.700000000000003), 
             ('20141223', 1.6000000000000014), 
             ('20141224', 3.700000000000003), 
             ('20141225', -2.3999999999999986), 
             ('20141226', -7.5), 
             ('20141227', -6.399999999999999), 
             ('20141228', -10.2), 
             ('20141229', 3.4000000000000057)]

DISPLAYED_MAXS = """Date        Carnarvon      Perth
20141220     26.9           28.7
20141221     33.6           29.6
20141222     36.7           30.0
20141223     30.5           32.1
20141224     28.9           32.6
20141225     34.3           31.9
20141226     40.9           33.4
20141227     41.4           35.0
20141228     41.5           31.3
20141229     32.3           35.7
"""

DISPLAYED_DIFFS = """Temperature differences between Perth and Carnarvon

Date      Temperature Differences
20141220    1.8
20141221   -4.0
20141222   -6.7
20141223    1.6
20141224    3.7
20141225   -2.4
20141226   -7.5
20141227   -6.4
20141228  -10.2
20141229    3.4
"""

TESTS = []
def test(function):
    # This is an awful hack, but it works
    TESTS.append(function)
    return function

##############
# TEST CASES #
##############

@test
def test_load_dates():
    return run_test('load_dates', (STATIONS,), DATES)

@test
def test_load_station_data():
    return run_test('load_station_data', ('Perth',), PERTH_DATA)

@test
def test_load_all_station_data():
    return run_test('load_all_stations_data', (STATIONS,), ALL_DATA)

@test
def test_temperature_diffs():
    return run_test('temperature_diffs', 
                    (ALL_DATA, DATES, STATIONS, 'Perth', 'Carnarvon', 
                     '20141220', '20141229'), DIFF_DATA)

@test
def test_display_maxs():
    return run_test('display_maxs', (STATIONS, DATES, ALL_DATA, '20141220', '20141229'), None, expected_stdout=DISPLAYED_MAXS)

@test
def test_display_diffs():
    return run_test('display_diffs', (DIFF_DATA, 'Perth', 'Carnarvon'), None, expected_stdout=DISPLAYED_DIFFS)



# If you would like to write your own test cases, do so here.
# Tests must have '@test' on the line above the function definition.
# Each test should return True/False based on whether the test passed.

# You can use the function run_test, which takes three arguments:
# 1) the name of the function to run,
# 2) a tuple of parameters to pass to the function, and
# 3) the expected return value.
# * if the function should print output (e.g. display), specify an
#   expected_stdout parameter, which is the string that should be printed.






######################################
# END TEST CASES                     #
# Support code for running the tests #
######################################

def strip_trailing_spaces(text):
    lines = text.split('\n')
    lines = [ln.rstrip() for ln in lines]
    return '\n'.join(lines)

def get_function(function_name, module=assign1):
    """Get a function from the assign1 module.
    If the function doesn't exist, return a function that raises a NameError.
    """
    def not_here(*args, **kwargs):
        raise NameError("Check that you have defined the {} function".format(function_name))
    return getattr(module, function_name, not_here)

def run_safely(f, args=()):
    """Run a function, and if an exception happens, don't die.
    Also report any output which was printed to stdout.

    Return (True, return_value, stdout) if no exception was raised,
    (False, sys.exc_info(), stdout) if there was an exception.
    """
    real_stdout, sys.stdout = sys.stdout, io.StringIO()
    try:
        result = f(*args)  # Call the function that's being tested
    except Exception as e:
        exception = True
        result = sys.exc_info()
    else:
        exception = False
    finally:
        output = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = real_stdout
    return (exception, result, output)

def format_function_call(f, args):
    """Make a function call look pretty"""
    arg_names = [arg[0] if isinstance(arg, tuple) else repr(arg) for arg in args]
    return "{f}({args})".format(f=f, args=', '.join(arg_names))

def run_test(f, args, expected, expected_stdout=''):
    """Run a test to see if a function does what it should. Return True if it passed.

    The function passes the test if and only if all of the following are true:
    * The function exists, and did not raise an exception
    * The return value equals the `expected` argument
    * The printed output equals `expected_stdout`

    run_test(str, tuple(objects), object, [str]) -> boolean
    """
    print()
    print(">>>", format_function_call(f, args))
    args = [arg[1] if isinstance(arg, tuple) else arg for arg in args]
    exc, result, stdout = run_safely(get_function(f), args)

    # Show the user any output to stdout, and any exception traceback
    # If an exception happened, the test fails.
    if stdout:
        print(stdout)
    if exc:
        traceback.print_exception(*result)
        return False

    # Check that stdout is correct
    if strip_trailing_spaces(stdout) != expected_stdout:
        #print(len(stdout), len(expected_stdout))
        print("Incorrect printed output - Expected:\n{}".format(expected_stdout), file=sys.stderr)
        return False

    # Show the user the return value
    if result is not None:
        pprint.pprint(result)
    # Check the return value is as expected
    if result == expected:
        return True
    else:
        print("Incorrect return value - Expected:", file=sys .stderr) 
        pprint.pprint(expected, sys.stderr)
        return False

def main():
    """Run all the tests."""
    score = 0
    for t in TESTS:
        result = t()
        if result:
            print("OK")
            score += 1
    total = len(TESTS)
    print()
    print()
    print("Passed {0} / {1} tests".format(score, total))
    print()
    print("NOTE: These tests are not comprehensive!")
    print("You should do further tests to check your code is correct.")

if __name__ == '__main__':
    main()
