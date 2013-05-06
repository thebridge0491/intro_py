# -*- coding: utf-8 -*-
'''Test cases for Classic module.'''
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import unittest, nose2
from nose2.tools.decorators import with_setup, with_teardown
from future.builtins import (ascii, filter, hex, map, oct, zip, range)

from {{parent}}.{{project}} import classic

def in_epsilon(val_a, val_b, tolerance=0.001):
    #return ((abs(val_a) - tolerance) <= abs(val_b) and
    #    (abs(val_a) + tolerance) >= abs(val_b))
    delta = abs(tolerance)
    #return (val_a - delta) <= val_b and (val_a + delta) >= val_b
    return (not (val_a + delta) < val_b) and (not (val_b + delta) < val_a)

def bound_values(*min_max_groups):
    avg_vals = [(min_m + max_m) // 2 for (min_m, max_m) in min_max_groups]
    axis_bounds = [(min_m, min_m + 1, (min_m + max_m) // 2, max_m - 1, max_m)
        for (min_m, max_m) in min_max_groups]
    bound_vals = [tuple(avg_vals[:ndx] + [el] + avg_vals[(ndx + 1):])
        for ndx, axis in enumerate(axis_bounds) for el in axis]
    return set(bound_vals)

def setUpModule():
    '''Set up (module-level) test fixtures, if any.'''
    print('Setup module: {0}'.format(__name__))

def tearDownModule():
    '''Tear down (module-level) test fixtures, if any.'''
    print('Teardown module: {0}'.format(__name__))

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
def test_fact():
	for fn1, num in [(f, n)
			for (n,) in bound_values(*[(0, 18)])
			# for n in [0, 9, 18]
			for f in [classic.fact_i, classic.fact_lp]]:
		assert ([1] + [a for a in [1] for b in range(1, num + 1)
			for a in [a * b]])[-1] == fn1(num)

@with_setup(setup_func1)
@with_teardown(teardown_func1)
def test_expt():
	for fn1, base, num in [(f, b, n)
			for (b, n) in bound_values(*[(2.0, 20.0), (3.0, 10.0)])
			# for b in [2.0, 11.0, 20.0] for n in [3.0, 6.0, 10.0]
			for f in [classic.expt_i, classic.expt_lp]]:
		#assert (base ** num) == fn1(base, num)
		assert in_epsilon(base ** num, fn1(base, num), 0.001 * (base ** num))
