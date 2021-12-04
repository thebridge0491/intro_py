# -*- coding: utf-8 -*-
'''New test case examples for `intro_py-scriptexplore` package.'''
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import sys, unittest
#from builtins import (ascii, filter, hex, map, oct, zip)

def setUpModule():
    #print('Setup module: {0}'.format(__name__))
    pass

def tearDownModule():
    #print('Teardown module: {0}'.format(__name__))
    pass

class TestNew(unittest.TestCase):
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
    
    def test_method(self):
        self.assertEqual(4, 2 * 2)
    
    @unittest.expectedFailure
    def test_failed_method(self):
        self.assertEqual(5, 2 * 2)
    
    @unittest.skip('ignoring test')
    def test_ignored_method(self):
        self.fail()
    
    @unittest.skipIf(1 == 1, 'conditionally ignoring test')
    def test_cond_ignored_method(self):
        self.fail()
    
    @unittest.skipUnless(sys.platform.startswith('win'), 'requires Windows')
    def test_specific_op_sys(self):
        self.fail()

    def test_expected_exception(self):
        with self.assertRaises(ZeroDivisionError):
            1 / 0   # raise Exception()
