# -*- coding: utf-8 -*-
'''Test properties for Classic module.'''
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import unittest #, operator
#from functools import reduce
#from builtins import (ascii, filter, hex, map, oct, zip, object, str, range)

from intro_py import util
from intro_py.foreignc import classic

try:
    from hypothesis import (given, note, settings, Verbosity, 
        strategies as st)
except ImportError as exc:
    raise unittest.SkipTest(__name__ + ': ' + repr(exc))


settings.register_profile('debug', settings(verbosity = Verbosity.
    normal, max_examples = 5))
settings.load_profile('debug')

def setUpModule():
    #print('Setup module: {0}'.format(__name__))
    pass

def tearDownModule():
    #print('Teardown module: {0}'.format(__name__))
    pass

class TestPropsClassic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #print('Setup class: {0}'.format(cls.__name__))
        pass

    @classmethod
    def tearDownClass(cls):
        #print('\nTeardown class: {0}'.format(cls.__name__))
        pass

    def setUp(self):
        #print('Setup method: {0}'.format(self._testMethodName))
        pass

    def tearDown(self):
        #print('Teardown method: {0}'.format(self.id().split('.')[-1]))
        pass

    @given(st.integers(min_value = 0, max_value = 18))
    def test_prop_fact(self, int_n):
        for fn1 in [classic.fact_i, classic.fact_lp]:
            #self.assertEqual((reduce(operator.mul, range(1, int_n + 1), 1)),
            #    fn1(int_n))
            self.assertEqual(([1] + [a for a in [1] for b in range(1, int_n + 1)
                for a in [a * b]])[-1], fn1(int_n))

    @given(st.integers(min_value = 1, max_value = 20),
        st.integers(min_value = 2, max_value = 10))
    def test_prop_expt(self, int_b, int_n):
        for fn1 in [classic.expt_i, classic.expt_lp]:
            base, num = float(int_b), float(int_n)
            #self.assertEqual(base ** num, fn1(base, num))
            self.assertTrue(util.in_epsilon(base ** num, fn1(base, num),
                0.001 * (base ** num)))
