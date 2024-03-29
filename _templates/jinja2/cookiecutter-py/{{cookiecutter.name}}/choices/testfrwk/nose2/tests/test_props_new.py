# -*- coding: utf-8 -*-
'''New test properties for `{{cookiecutter.parent}}{{cookiecutter.separator}}{{cookiecutter.project}}` package.'''
from __future__ import (absolute_import, division, print_function,
	unicode_literals)

import unittest, nose2
from future.builtins import (ascii, filter, hex, map, oct, zip, object, str)

try:
	from hypothesis import (given, note, settings, Verbosity, 
		strategies as st)
except ImportError as exc:
	raise unittest.SkipTest(__name__ + ': ' + repr(exc))


settings.register_profile('debug', settings(verbosity = Verbosity.
	normal, max_examples = 5, max_iterations = 10))
settings.load_profile('debug')

def setUpModule():
	#print('Setup module: {0}'.format(__name__))
	pass

def tearDownModule():
	#print('Teardown module: {0}'.format(__name__))
	pass

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

#@with_setup_teardown(setup_func1, teardown_func1)
@with_setup(setup_func1)
@with_teardown(teardown_func1)
@given(st.integers(), st.integers())
def test_ints_are_commutative(int_x, int_y):
	assert (int_x + int_y) == (int_y + int_x)

@with_setup(setup_func1)
@with_teardown(teardown_func1)
@given(int_x = st.integers(), int_y = st.integers())
def test_ints_cancel(int_x, int_y):
	assert ((int_x + int_y) - int_y) == int_x

@with_setup(setup_func1)
@with_teardown(teardown_func1)
@given(st.lists(st.integers()))
def test_reverse_reverse_id(xss):
	yss = list(reversed(xss))
	yss.reverse()
	assert xss == yss

@with_setup(setup_func1)
@with_teardown(teardown_func1)
@given(st.lists(st.integers()), st.randoms())
def test_shuffle_is_noop(xss, rnd):
	yss = list(xss)
	rnd.shuffle(yss)
	note("Shuffle: {0}".format(yss))
	assert xss == yss

@with_setup(setup_func1)
@with_teardown(teardown_func1)
@given(st.tuples(st.booleans(), st.text()))
def test_tuple_bool_text(tup):
	assert len(tup) == 2
	assert isinstance(tup[0], bool)
	assert isinstance(tup[1], str)

with settings(timeout = 1):
	@with_setup(setup_func1)
	@with_teardown(teardown_func1)
	@given(st.characters(), st.characters())
	def test_chars_timeout(char_a, char_b):
		import time
		time.sleep(2)
		assert isinstance(char_a, str)
		assert isinstance(char_b, str)
