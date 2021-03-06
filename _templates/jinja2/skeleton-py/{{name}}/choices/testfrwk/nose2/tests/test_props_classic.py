# -*- coding: utf-8 -*-
'''Test properties for Classic module.'''
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import unittest, nose2 #, operator
#from functools import reduce
from nose2.tools.decorators import with_setup, with_teardown
from future.builtins import (ascii, filter, hex, map, oct, zip, object, str,
    range)

from {{parent}}.{{project}} import classic

try:
    from hypothesis import (given, note, settings, Verbosity, 
        strategies as st)
except ImportError as exc:
    raise unittest.SkipTest(__name__ + ': ' + repr(exc))


settings.register_profile('debug', settings(verbosity = Verbosity.
    normal, max_examples = 5, max_iterations = 10))
settings.load_profile('debug')

def in_epsilon(val_a, val_b, tolerance=0.001):
    #return ((abs(val_a) - tolerance) <= abs(val_b) and
    #    (abs(val_a) + tolerance) >= abs(val_b))
    delta = abs(tolerance)
    #return (val_a - delta) <= val_b and (val_a + delta) >= val_b
    return (not (val_a + delta) < val_b) and (not (val_b + delta) < val_a)

def setUpModule():
    #print('Setup module: {0}'.format(__name__))
    pass

def tearDownModule():
    #print('Teardown module: {0}'.format(__name__))
    pass

def with_setup_teardown(setup_func, teardn_func, setup_addon=None,
        teardn_addon=None):
    def setup_func_addon(testcs):
        setup_func()
        print('\n##### Setup ({0}) {1} #####'.format(__name__, 
            testcs.__name__))
    def teardn_func_addon(testcs):
        teardn_func()
        print('\n##### Teardown ({0}) {1} #####'.format(__name__, 
            testcs.__name__))
    def decorator(testcs):
        testcs.setup = lambda : setup_func_addon(testcs)
        testcs.teardown = lambda : teardn_func_addon(testcs)
        return testcs
    return decorator

def setup_func1():
    pass

def teardown_func1():
    pass

#@with_setup_teardown(setup_func1, teardown_func1)
@with_setup(setup_func1)
@with_teardown(teardown_func1)
@given(st.integers(min_value = 0, max_value = 18))
def test_prop_fact(int_n):
	for fn1 in [classic.fact_i, classic.fact_lp]:
		#assert (reduce(operator.mul, range(1, int_n + 1), 1)) == fn1(int_n)
		assert ([1] + [a for a in [1] for b in range(1, int_n + 1)
			for a in [a * b]])[-1] == fn1(int_n)

@with_setup(setup_func1)
@with_teardown(teardown_func1)
@given(st.integers(min_value = 1, max_value = 20),
	st.integers(min_value = 2, max_value = 10))
def test_prop_expt(int_b, int_n):
	for fn1 in [classic.expt_i, classic.expt_lp]:
		base, num = float(int_b), float(int_n)
		#assert (base ** num) == fn1(base, num)
		assert in_epsilon(base ** num, fn1(base, num), 0.001 * (base ** num))
