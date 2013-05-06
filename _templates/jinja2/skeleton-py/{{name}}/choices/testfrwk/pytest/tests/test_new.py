# -*- coding: utf-8 -*-
'''New test case examples for `{{parent}}{{separator}}{{project}}` package.'''
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import pytest
from future.builtins import (ascii, filter, hex, map, oct, zip, object)

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

def test_method(fixture_func1):
    assert 4 == 2 * 2

@pytest.mark.xfail
def test_failed_method(fixture_func1):
    assert 5 == 2 * 2

@pytest.mark.skipif(True, reason='ignoring test')
def test_ignored_method(fixture_func1):
    assert False

@pytest.mark.skipif(1 == 1, reason = 'conditionally ignoring test')
def test_cond_ignored_method(fixture_func1):
    assert False

def test_expected_exception(fixture_func1):
    with pytest.raises(ZeroDivisionError):
        1 / 0   # raise Exception()

@pytest.mark.timeout(1)
def test_timeout(fixture_func1):
    import time
    time.sleep(2)
    assert True

class TestNew(object):
    @classmethod
    def setup_class(cls):
        print("Setup class: {0}".format(cls.__name__))

    @classmethod
    def teardown_class(cls):
        print("\nTeardown class: {0}".format(cls.__name__))

    def setup_method(self, method):
        print("Setup method: {0}".format(method.__name__))

    def teardown_method(self, method):
        print("\nTeardown method: {0}".format(method.__name__))

    @pytest.fixture
    def fixture_method1(self, request):
        print("Setup method1 (EXTRA) {0}".format(request.function.__name__))

        def fin():
            print("\nTeardown method1 (EXTRA) {0}".format(request.function.__name__))
        request.addfinalizer(fin)

    def test_classmethod(self, fixture_method1):
        assert 4 == 2 * 2
