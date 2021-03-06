# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import unittest, nose2
from nose2.tools.decorators import with_setup, with_teardown
from future.builtins import (ascii, filter, hex, map, oct, zip)

class LayerModule(object):
    @classmethod
    def setUp(cls):
        print('SetUp module: {0}'.format(__name__))

    @classmethod
    def tearDown(cls):
        print('\nTearDown module: {0}'.format(__name__))

class TestLayerNew(LayerModule):
    @classmethod
    def setUp(cls):
        print("Setup class: {0}".format(cls.__name__))

    @classmethod
    def tearDown(cls):
        print("\nTeardown class: {0}".format(cls.__name__))

    @classmethod
    def testSetUp(cls, test):
        print('Setup method: {0}'.format(test._testMethodName))

    @classmethod
    def testTearDown(cls, test):
        print('\nTeardown method: {0}'.format(test.id().split('.')[-1]))

class TestNew(unittest.TestCase):
    layer = TestLayerNew  # enable nose2 option: --plugin=nose2.plugins.layers

    def test_method(self):
        self.assertTrue(4 == 2 * 2)
