# -*- coding: utf-8 -*-
'''Test cases for Classic module.'''from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import pytest
from future.builtins import (ascii, filter, hex, map, oct, zip, object, range)

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

def setup_module(module):
    print("\nSetup module: {0}".format(module.__name__))

def teardown_module(module):
    print("\nTeardown module: {0}".format(module.__name__))

def setup_function(function):
    print("Setup function: {0}".format(function.__name__))

def teardown_function(function):
    print("\nTeardown function: {0}".format(function.__name__))

@pytest.fixture
def fixture_func1(request):
    print("Setup function (Fixture1): {0}".format(request.function.__name__))

    def fin():
        print("\nTeardown function (Fixture1): {0}".format(request.function.__name__))
    request.addfinalizer(fin)

def test_fact(fixture_func1):
	for fn1, num in [(f, n)
			for (n,) in bound_values(*[(0, 18)])
			# for n in [0, 9, 18]
			for f in [classic.fact_i, classic.fact_lp]]:
		assert ([1] + [a for a in [1] for b in range(1, num + 1)
			for a in [a * b]])[-1] == fn1(num)

def test_expt(fixture_func1):
	for fn1, base, num in [(f, b, n)
			for (b, n) in bound_values(*[(2.0, 20.0), (3.0, 10.0)])
			# for b in [2.0, 11.0, 20.0] for n in [3.0, 6.0, 10.0]
			for f in [classic.expt_i, classic.expt_lp]]:
		#assert (base ** num) == fn1(base, num)
		assert in_epsilon(base ** num, fn1(base, num), 0.001 * (base ** num))
