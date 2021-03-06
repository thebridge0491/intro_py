# -*- coding: utf-8 -*-
'''Test cases for Classic module.'''
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import unittest
from future.builtins import (ascii, filter, hex, map, oct, zip, range)

from {{cookiecutter.parent}}.{{cookiecutter.project}} import classic

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

class TestClassic(unittest.TestCase):
    '''Tests for Classic module.'''

    @classmethod
    def setUpClass(cls):
        '''Set up (class-level) test fixtures, if any.'''
        print('Setup class: {0}'.format(cls.__name__))

    @classmethod
    def tearDownClass(cls):
        '''Tear down (class-level) test fixtures, if any.'''
        print('\nTeardown class: {0}'.format(cls.__name__))
    
    def setUp(self):
        '''Set up test fixtures, if any.'''
        print('Setup method: {0}'.format(self._testMethodName))

    def tearDown(self):
        '''Tear down test fixtures, if any.'''
        print('Teardown method: {0}'.format(self.id().split('.')[-1]))

    def test_fact(self):
        for fn1, num in [(f, n)
                for (n,) in bound_values(*[(0, 18)])
                # for n in [0, 9, 18]
                for f in [classic.fact_i, classic.fact_lp]]:
            self.assertTrue(([1] + [a for a in [1] for b in range(1, num + 1)
                for a in [a * b]])[-1] == fn1(num))

    def test_expt(self):
        for fn1, base, num in [(f, b, n)
                for (b, n) in bound_values(*[(2.0, 20.0), (3.0, 10.0)])
                # for b in [2.0, 11.0, 20.0] for n in [3.0, 6.0, 10.0]
                for f in [classic.expt_i, classic.expt_lp]]:
            #self.assertEqual(base ** num, fn1(base, num))
            self.assertTrue(in_epsilon(base ** num, fn1(base, num),
                0.001 * (base ** num)))
