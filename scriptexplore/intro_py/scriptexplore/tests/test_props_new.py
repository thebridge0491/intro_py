# -*- coding: utf-8 -*-
'''New test property examples for `intro_py-scriptexplore` package.'''
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import unittest
from future.builtins import (ascii, filter, hex, map, oct, zip, object, str)

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

class TestPropsNew(unittest.TestCase):
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

    @given(st.integers(), st.integers())
    def test_ints_are_commutative(self, int_x, int_y):
        self.assertEqual(int_x + int_y, int_y + int_x)

    @given(int_x = st.integers(), int_y = st.integers())
    def test_ints_cancel(self, int_x, int_y):
        self.assertEqual((int_x + int_y) - int_y, int_x)

    @given(st.lists(st.integers()))
    def test_reverse_reverse_id(self, xss):
        yss = list(reversed(xss))
        yss.reverse()
        self.assertEqual(xss, yss)

    @given(st.lists(st.integers()), st.randoms())
    def test_shuffle_is_noop(self, xss, rnd):
        yss = list(xss)
        rnd.shuffle(yss)
        note("Shuffle: {0}".format(yss))
        self.assertEqual(xss, yss)

    @given(st.tuples(st.booleans(), st.text()))
    def test_tuple_bool_text(self, tup):
        self.assertEqual(len(tup), 2)
        self.assertTrue(isinstance(tup[0], bool))
        self.assertTrue(isinstance(tup[1], str))
