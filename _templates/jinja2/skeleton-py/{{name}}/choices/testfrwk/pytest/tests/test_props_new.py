# -*- coding: utf-8 -*-
'''New test property examples for `{{parent}}{{separator}}{{project}}` package.'''
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import pytest
from future.builtins import (ascii, filter, hex, map, oct, zip, object, str)

try:
    from hypothesis import (given, note, settings, Verbosity, 
        strategies as st)
except ImportError as exc:
    pytestmark = pytest.mark.skipif(True, reason=__name__ + ': ' + repr(exc))


settings.register_profile('debug', settings(verbosity = Verbosity.
    normal, max_examples = 5, max_iterations = 10))
settings.load_profile('debug')

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

@given(st.integers(), st.integers())
def test_ints_are_commutative(int_x, int_y):
    assert int_x + int_y == int_y + int_x

@given(int_x = st.integers(), int_y = st.integers())
def test_ints_cancel(int_x, int_y):
    assert ((int_x + int_y) - int_y) == int_x

@given(st.lists(st.integers()))
def test_reverse_reverse_id(xss):
    yss = list(reversed(xss))
    yss.reverse()
    assert xss == yss

@given(st.lists(st.integers()), st.randoms())
def test_shuffle_is_noop(xss, rnd):
    yss = list(xss)
    rnd.shuffle(yss)
    note("Shuffle: {0}".format(yss))
    assert xss == yss

@given(st.tuples(st.booleans(), st.text()))
def test_tuple_bool_text(tup):
    assert len(tup) == 2
    assert isinstance(tup[0], bool)
    assert isinstance(tup[1], str)

with settings(timeout = 1):
    @given(st.characters(), st.characters())
    def test_chars_timeout(char_a, char_b):
        import time
        time.sleep(2)
        assert isinstance(char_a, str)
        assert isinstance(char_b, str)
