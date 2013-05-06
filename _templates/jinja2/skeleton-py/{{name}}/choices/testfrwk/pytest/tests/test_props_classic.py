# -*- coding: utf-8 -*-
'''Test properties for Classic module.'''
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import pytest #, operator
#from functools import reduce
from future.builtins import (ascii, filter, hex, map, oct, zip, object, str,
    range)

from {{parent}}.{{project}} import classic

try:
    from hypothesis import (given, note, settings, Verbosity, 
        strategies as st)
except ImportError as exc:
    pytestmark = pytest.mark.skipif(True, reason=__name__ + ': ' + repr(exc))


settings.register_profile('debug', settings(verbosity = Verbosity.
    normal, max_examples = 5, max_iterations = 10))
settings.load_profile('debug')

def in_epsilon(val_a, val_b, tolerance=0.001):
    #return ((abs(val_a) - tolerance) <= abs(val_b) and
    #    (abs(val_a) + tolerance) >= abs(val_b))
    delta = abs(tolerance)
    #return (val_a - delta) <= val_b and (val_a + delta) >= val_b
    return (not (val_a + delta) < val_b) and (not (val_b + delta) < val_a)

def setup_module(module):
    #print("\nSetup module: {0}".format(module.__name__))
    pass

def teardown_module(module):
    #print("\nTeardown module: {0}".format(module.__name__))
    pass

def setup_function(function):
    #print("Setup function: {0}".format(function.__name__))
    pass

def teardown_function(function):
    #print("\nTeardown function: {0}".format(function.__name__))
    pass

@pytest.fixture
def fixture_func1(request):
    print("Setup function (Fixture1): {0}".format(request.function.__name__))

    def fin():
        print("\nTeardown function (Fixture1): {0}".format(request.function.__name__))
    request.addfinalizer(fin)

@given(st.integers(min_value = 0, max_value = 18))
def test_prop_fact(int_n):
	for fn1 in [classic.fact_i, classic.fact_lp]:
		#assert (reduce(operator.mul, range(1, int_n + 1), 1)) == fn1(int_n)
		assert ([1] + [a for a in [1] for b in range(1, int_n + 1)
			for a in [a * b]])[-1] == fn1(int_n)

@given(st.integers(min_value = 1, max_value = 20),
	st.integers(min_value = 2, max_value = 10))
def test_prop_expt(int_b, int_n):
	for fn1 in [classic.expt_i, classic.expt_lp]:
		base, num = float(int_b), float(int_n)
		#assert (base ** num) == fn1(base, num)
		assert in_epsilon(base ** num, fn1(base, num), 0.001 * (base ** num))
