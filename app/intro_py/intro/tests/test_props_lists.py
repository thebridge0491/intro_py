# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import unittest
from functools import reduce
from future.builtins import (ascii, filter, hex, map, oct, zip)

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

def _flip_func(func, is_flipped=True):
    return (lambda *args: func(*reversed(args))) if is_flipped else func

def is_ordered(xss, is_rev=False):
    import operator
    
    def iter(rst, acc):
        return acc if 1 >= len(rst) else iter(rst[1:],
            acc and _flip_func(operator.le, is_rev)(rst[0], rst[1]))
    return iter(xss, True)

class TestPropsLists(unittest.TestCase):
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

    @given(st.lists(st.integers()))
    def test_prop_equal(self, xss):
        yss = xss[:]
        self.assertEqual(yss, xss)
        self.assertTrue(reduce(lambda a_mss, e: (a_mss[0] and e == a_mss[1][0],
            a_mss[1][1:]), xss, (True, yss))[0])

    @given(st.lists(st.integers()))
    def test_prop_notequal(self, xss):
        yss = xss[:] + [100]
        self.assertNotEqual(yss, xss)
        self.assertTrue(reduce(lambda a_mss, e: (a_mss[0] and e == a_mss[1][0],
            a_mss[1][1:]), xss, (True, yss))[0])
        #self.assertTrue(reduce(lambda (a, mss), e: (a and e == mss[0], 
        #    mss[1:]), xss, (True, yss))[0)

    @given(st.lists(st.integers()), st.lists(st.integers()))
    def test_prop_append(self, xss, yss):
        zss = xss + yss
        self.assertEqual(zss[len(xss):], yss)
        self.assertEqual(zss[:len(xss)], xss)

    @given(st.lists(st.integers()))
    def test_prop_rev_rev(self, xss):
        self.assertEqual(list(reversed(list(reversed(xss)))), xss)

    @given(st.lists(st.integers()))
    def test_prop_filter(self, xss):
        def pred1(x):
            return 0 == x % 2
        yss = list(filter(pred1, xss))
        self.assertEqual(list(filter(lambda x: not pred1(x), yss)), [])
        self.assertTrue(reduce(lambda a, e: a and pred1(e), yss, True))

    @given(st.lists(st.integers()))
    def test_prop_map(self, xss):
        def proc1(x):
            return x + 2
        yss = list(map(proc1, xss))
        self.assertTrue(reduce(lambda a_mss, e: (a_mss[0] and proc1(e) == a_mss[1][0],
            a_mss[1][1:]), xss, (True, yss))[0])

    @given(st.lists(st.integers()))
    def test_prop_sort_is_ordered(self, xss):
        self.assertTrue(is_ordered(list(sorted(xss))))

    @given(st.lists(st.integers()))
    def test_prop_revsort_is_revordered(self, xss):
        self.assertTrue(is_ordered(list(reversed(list(sorted(xss)))), True))
