# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import unittest
#from builtins import (ascii, filter, hex, map, oct, zip, dict, range)

LST, REVLST = list(range(0, 5)), list(range(4, -1, -1))

def setUpModule():
    #print('Setup module: {0}'.format(__name__))
    pass

def tearDownModule():
    #print('Teardown module: {0}'.format(__name__))
    pass

class TestCollections(unittest.TestCase):
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
    
    def test_lists(self):
        self.assertEqual(list((1,)), [1])
        self.assertEqual(LST, [0, 1, 2, 3, 4])
        self.assertNotEqual([], [0, 1, 2])
        self.assertEqual(0, len([]))
        self.assertEqual([2, 1, 0][0], 2)
        self.assertEqual(len([2, 1, 0]), 3)
        self.assertEqual([2, 1, 0] + [9, 9, 9], [2, 1, 0, 9, 9, 9])
        self.assertEqual(list(reversed([2, 1, 0])), [0, 1, 2])
        self.assertTrue(1 in [2, 1, 0])
        self.assertEqual(list(filter(lambda el: 0 == el % 2, LST)), [0, 2, 4])
        lst1 = [1, 2, 3, 2]
        lst1.remove(2)
        self.assertEqual(lst1, [1, 3, 2])
        self.assertEqual(list(map(lambda el: el + 2, LST)), [2, 3, 4, 5, 6])
        self.assertEqual(sorted([3, 2, 4, 0, 1], reverse=True), REVLST)
        self.assertEqual(sorted([3, 2, 4, 0, 1], key=lambda x: -x), REVLST)
    
    def test_sets(self):
        setA = set()
        setA.add('i')
        self.assertEqual(setA, {'i'})
        set1, set2 = {'k', 'p', 'a', 'e', 'u', 'k', 'a'}, {'q', 'p', 'z', 'u'}
        self.assertEqual(set(('a',)), {'a'})
        self.assertEqual(sorted(set1), ['a', 'e', 'k', 'p', 'u'])
        self.assertEqual(sorted(set1 | set2), ['a', 'e', 'k', 'p', 'q', 'u', 'z'])
        self.assertEqual(sorted(set1 & set2), ['p', 'u'])
        self.assertEqual(sorted(set1 - set2), ['a', 'e', 'k'])
        self.assertEqual(sorted(set1 ^ set2), ['a', 'e', 'k', 'q', 'z'])
    
    def test_dicts(self):
        dictA = dict()
        self.assertEqual(dictA, {})
        self.assertEqual(dict([('ltr 99', 'M')]), {'ltr 99': 'M'})
        self.assertEqual(dict(zip(['ltr 99'], ['M'])), {'ltr 99': 'M'})
        dict1 = dict(zip(['ltr 01', 'ltr 02', 'ltr 03'], ['a', 'b', 'c']))
        self.assertEqual(len(dict1), 3)
        dict1['ltr 20'] = 'Z'
        self.assertTrue('ltr 20' in dict1)
        self.assertEqual(dict1.get('ltr 02', 'M'), 'b')
        del dict1['ltr 02']
        self.assertTrue('ltr 02' not in dict1)
        self.assertEqual(sorted(dict1.items()), [('ltr 01', 'a'), ('ltr 03', 'c'),
            ('ltr 20', 'Z')])
    
    def test_deques(self):
        from collections import deque
        dequeA = deque()
        self.assertEqual(0, len(dequeA))
        deque1 = deque([25.7, 0.1, 78.5, 52.3])
        self.assertEqual(deque1[0], 25.7)
        deque1.append(-5.0)
        self.assertEqual(deque1.popleft(), 25.7)
        self.assertEqual(sorted(deque1), [-5.0, 0.1, 52.3, 78.5])
    
    def test_heaps(self):
        import heapq
        heapA = []
        self.assertEqual(len(heapA), 0)
        heap1 = [25.7, 0.1, 78.5, 52.3]
        heapq.heapify(heap1)
        heapq.heappush(heap1, -5.0)
        self.assertEqual(sorted(heap1), [-5.0, 0.1, 25.7, 52.3, 78.5])
        self.assertEqual(heapq.heappop(heap1), -5.0)
        self.assertEqual(heap1[0], 0.1)
