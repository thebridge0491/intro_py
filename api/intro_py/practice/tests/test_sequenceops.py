# -*- coding: utf-8 -*-
'''Test cases for Sequenceops module.'''
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import unittest
from future.builtins import (ascii, filter, hex, map, oct, zip, range)

from intro_py import util
from intro_py.practice import sequenceops as seqops

LST, REVLST = list(range(0, 5)), list(range(4, -1, -1))

def setUpModule():
    '''Set up (module-level) test fixtures, if any.'''
    print('Setup module: {0}'.format(__name__))

def tearDownModule():
    '''Tear down (module-level) test fixtures, if any.'''
    print('Teardown module: {0}'.format(__name__))

class TestSequenceops(unittest.TestCase):
    '''Tests for Sequenceops module.'''

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

    def test_index(self):
        for fn1, xss in [(f, l) for l in [LST, REVLST]
                for f in [seqops.index_i, seqops.index_lp]]:
            self.assertEqual(xss.index(3), fn1(3, xss))
            self.assertEqual(-1, fn1(-20, xss))

    def test_copy_of(self):
        for fn1, xss in [(f, l) for l in [LST, REVLST]
                for f in [seqops.copy_of_i, seqops.copy_of_r, seqops.copy_of_lp]]:
            self.assertEqual(xss[:], fn1(xss))

    def test_reverse(self):
        for fn1, xss in [(f, l) for l in [LST, REVLST]
                for f in [seqops.reverse_i, seqops.reverse_r, seqops.reverse_lp]]:
            self.assertEqual(list(reversed(seqops.copy_of_i(xss))), fn1(xss))
