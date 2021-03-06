# -*- coding: utf-8 -*-
'''New test cases for `{{cookiecutter.parent}}{{cookiecutter.separator}}{{cookiecutter.project}}` package.'''
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import sys, unittest, nose2
from nose2.tools.decorators import with_setup, with_teardown
from future.builtins import (ascii, filter, hex, map, oct, zip)

def setUpModule():
    print('Setup module: {0}'.format(__name__))

def tearDownModule():
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

#@with_setup(setup_func1)
#@with_teardown(teardown_func1)
@with_setup_teardown(setup_func1, teardown_func1)
def test_method():
    assert 4 == 2 * 2

@with_setup_teardown(setup_func1, teardown_func1)
@unittest.expectedFailure
def test_failed_method():
    assert 5 == 2 * 2

@with_setup_teardown(setup_func1, teardown_func1)
@unittest.skip('ignoring test')
def test_ignored_method():
    assert False

@with_setup_teardown(setup_func1, teardown_func1)
@unittest.skipIf(1 == 1, 'conditionally ignoring test')
def test_cond_ignored_method():
    assert False

@with_setup_teardown(setup_func1, teardown_func1)
@unittest.skipUnless(sys.platform.startswith('win'), 'requires Windows')
def test_specific_op_sys():
    assert False

@with_setup_teardown(setup_func1, teardown_func1)
@unittest.expectedFailure
def test_expected_exception():
    1 / 0   # raise Exception()

class TestNew(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setup class: {0}'.format(cls.__name__))

    @classmethod
    def tearDownClass(cls):
        print('\nTeardown class: {0}'.format(cls.__name__))

    def setUp(self):
        print('Setup method: {0}'.format(self._testMethodName))

    def tearDown(self):
        print('Teardown method: {0}'.format(self.id().split('.')[-1]))
    
    def test_classmethod(self):
        self.assertEqual(4, 2 * 2)
