# -*- coding: utf-8 -*-
'''Test properties for Sequenceops module.'''
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import unittest #, operator
#from functools import reduce
from future.builtins import (ascii, filter, hex, map, oct, zip, object, str,
    range)

from intro_py import util
from intro_py.practice import sequenceops as seqops

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

class TestPropsSequenceops(unittest.TestCase):
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

    @given(st.data(), st.lists(st.integers(), min_size = 1))
    def test_prop_index(self, data, xss):
        data1 = data.draw(st.sampled_from(tuple(xss)))
        for fn1 in [seqops.index_i, seqops.index_lp]:
            self.assertEqual(xss.index(data1), fn1(data1, xss))
            self.assertEqual(-1, fn1(-20, list(range(0, 20))))

    @given(st.lists(st.integers()))
    def test_prop_copy_of(self, xss):
        for fn1 in [seqops.copy_of_i, seqops.copy_of_r, seqops.copy_of_lp]:
            self.assertEqual(xss[:], fn1(xss))

    @given(st.lists(st.integers()))
    def test_prop_reverse(self, xss):
        for fn1 in [seqops.reverse_i, seqops.reverse_r, seqops.reverse_lp]:
            self.assertEqual(list(reversed(seqops.copy_of_i(xss))), fn1(xss))
