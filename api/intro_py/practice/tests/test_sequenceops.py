# -*- coding: utf-8 -*-
'''Test cases for Sequenceops module.'''
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import unittest
from functools import reduce
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

    def test_tabulate(self):
        from itertools import count
        def proc_id(el): return el
        def proc1(el): return 32 // (2 ** el)
        for func, cnt in [(proc_id, 5), (proc1, 5)]:
            ans_gen = map(func, count())
            ans = [next(ans_gen) for i in range(cnt)]
            for fn1 in [seqops.tabulate_i, seqops.tabulate_r, seqops.tabulate_lp]:
                self.assertEqual(ans, fn1(func, cnt))

    def test_length(self):
        for xss in [list(range(len1)) for len1 in [0, 3, 5, 7]]:
            ans = len(xss)
            for fn1 in [seqops.length_i, seqops.length_r, seqops.length_lp]:
                self.assertEqual(ans, fn1(xss))

    def test_nth(self):
        for xss in [LST, REVLST]:
            ans = xss[3]
            for fn1 in [seqops.nth_i, seqops.nth_r, seqops.nth_lp]:
                self.assertEqual(ans, fn1(3, xss))

    def test_index(self):
        for xss in [LST, REVLST]:
            ans = xss.index(3)
            for fn1 in [seqops.index_i, seqops.index_r, seqops.index_lp]:
                self.assertEqual(ans, fn1(3, xss))
                self.assertEqual(-1, fn1(-20, xss))

    def test_find(self):
        for xss in [LST, REVLST]:
            ans = 3
            for fn1 in [seqops.find_i, seqops.find_r, seqops.find_lp]:
                self.assertEqual(ans, fn1(3, xss))

    def test_min_max(self):
        for xss in [LST, REVLST]:
            ans_min, ans_max = min(xss), max(xss)
            for (fn_min, fn_max) in [(seqops.min_i, seqops.max_i),
                    (seqops.min_r, seqops.max_r), (seqops.min_lp, seqops.max_lp)]:
                self.assertEqual(ans_min, fn_min(xss))
                self.assertEqual(ans_max, fn_max(xss))

    def test_reverse(self):
        for xss in [LST, REVLST]:
            ans = list(reversed(xss[:]))
            for fn1 in [seqops.reverse_i, seqops.reverse_r, seqops.reverse_lp]:
                self.assertEqual(ans, fn1(xss))

    def test_reverse_mut(self):
        for xss in [LST, REVLST]:
            exp_lst = xss[:]
            exp_lst.reverse()
            for fn1 in [seqops.reverse_mut_i, seqops.reverse_mut_lp]:
                act_lst = xss[:]
                fn1(act_lst)
                self.assertEqual(exp_lst, act_lst)

    def test_copy_of(self):
        for xss in [LST, REVLST]:
            ans = xss[:]
            for fn1 in [seqops.copy_of_i, seqops.copy_of_r, seqops.copy_of_lp]:
                self.assertEqual(ans, fn1(xss))

    def test_take_drop(self):
        for xss in [LST, REVLST]:
            ans_take = reduce(lambda a, i_e: a + [i_e[1]] if 3 > i_e[0] else a,
                enumerate(xss), [])
            ans_drop = reduce(lambda a, i_e: a + [i_e[1]] if 3 <= i_e[0] else a,
                enumerate(xss), [])
            for (fn_take, fn_drop) in [(seqops.take_i, seqops.drop_i),
                    (seqops.take_lp, seqops.drop_lp)]:
                self.assertEqual(ans_take, fn_take(3, xss))
                self.assertEqual(ans_drop, fn_drop(3, xss))
            for fn1 in [seqops.split_at_i, seqops.split_at_lp]:
                res = fn1(3, xss)
                self.assertEqual(ans_take, res[0])
                self.assertEqual(ans_drop, res[1])

    def test_any_all(self):
        def pred1(el): return 0 == el % 2
        def pred2(el): return [] != el
        for (pred, xss) in [(pred1, [1, 2, 3]), (pred2, [[1, 2], [], [3, 4]]),
                (pred1, [6, 2, 4]), (pred2, [[1, 2], [5], [3, 4]])]:
            ans_any = reduce(lambda a, e: a or pred(e), xss, False)
            ans_all = reduce(lambda a, e: a and pred(e), xss, True)
            for (fn_any, fn_all) in [(seqops.any_i, seqops.all_i),
                    (seqops.any_r, seqops.all_r), (seqops.any_lp, seqops.all_lp)]:
                self.assertEqual(ans_any, fn_any(pred, xss))
                self.assertEqual(ans_all, fn_all(pred, xss))

    def test_map(self):
        def proc(el): return el + 2
        for xss in [LST, REVLST]:
            ans = list(map(proc, xss))
            for fn1 in [seqops.map_i, seqops.map_r, seqops.map_lp]:
                self.assertEqual(ans, fn1(proc, xss))

    def test_foreach(self):
        def proc(el): print('{0} '.format(el))
        for xss in [LST, REVLST]:
            ans = None
            for fn1 in [seqops.foreach_i, seqops.foreach_r, seqops.foreach_lp]:
                self.assertEqual(ans, fn1(proc, xss))

    def test_filter_remove(self):
        def pred1(el): return 0 == el % 2
        for xss in [LST, REVLST]:
            ans_filter = reduce(lambda a, e: a + [e] if pred1(e) else a,
                xss, [])
            ans_remove = reduce(lambda a, e: a + [e] if not pred1(e) else a,
                xss, [])
            for (fn_f, fn_r) in [(seqops.filter_i, seqops.remove_i),
                    (seqops.filter_r, seqops.remove_r),
                    (seqops.filter_lp, seqops.remove_lp)]:
                self.assertEqual(ans_filter, fn_f(pred1, xss))
                self.assertEqual(ans_remove, fn_r(pred1, xss))
            for fn1 in [seqops.partition_i, seqops.partition_r,
                    seqops.partition_lp]:
                res = fn1(pred1, xss)
                self.assertEqual(ans_filter, res[0])
                self.assertEqual(ans_remove, res[1])

    def test_fold_left(self):
        def corp1(a, e): return a + e
        def corp2(a, e): return a - e
        for xss in [LST, REVLST]:
            ans1 = reduce(corp1, xss, 0)
            ans2 = reduce(corp2, xss, 0)
            for fn1 in [seqops.fold_left_i, seqops.fold_left_r,
                    seqops.fold_left_lp]:
                self.assertEqual(ans1, fn1(corp1, 0, xss))
                self.assertEqual(ans2, fn1(corp2, 0, xss))

    def test_fold_right(self):
        def proc1(e, a): return e + a
        def proc2(e, a): return e - a
        for xss in [LST, REVLST]:
            ans1 = reduce(lambda a, e: proc1(e, a), reversed(xss), 0)
            ans2 = reduce(lambda a, e: proc2(e, a), reversed(xss), 0)
            for fn1 in [seqops.fold_right_i, seqops.fold_right_r,
                    seqops.fold_right_lp]:
                self.assertEqual(ans1, fn1(proc1, xss, 0))
                self.assertEqual(ans2, fn1(proc2, xss, 0))

    def test_unfold_right(self):
        def func1(fst_snd):
            (fst, snd) = fst_snd
            if 0 == snd: return None
            return (fst, (fst + 1, snd - fst))
        def func2(fst_snd):
            (fst, snd) = fst_snd
            if 0 == snd: return None
            return (fst, (fst + 1, fst - snd))
        for fn1 in [seqops.unfold_right_i, seqops.unfold_right_lp]:
            self.assertEqual([4, 3, 2, 1, 0], fn1(func1, (0, 10)))
            self.assertEqual([4, 3, 2, 1, 0], fn1(func2, (0, 2)))

    def test_unfold_left(self):
        def func1(fst_snd):
            (fst, snd) = fst_snd
            if 0 == snd: return None
            return (fst, (fst + 1, snd - fst))
        def func2(fst_snd):
            (fst, snd) = fst_snd
            if 0 == snd: return None
            return (fst, (fst + 1, fst + snd))
        for fn1 in [seqops.unfold_left_r, seqops.unfold_left_lp]:
            self.assertEqual([0, 1, 2, 3, 4], fn1(func1, (0, 10)))
            self.assertEqual([0, 1, 2, 3, 4], fn1(func2, (0, -10)))


    def test_is_ordered(self):
        for xss in [LST, REVLST, ['a', 'b', 'b', 'c'], ['c', 'b', 'a', 'a']]:
            ansrev = reduce(lambda a, i: a and xss[i] >= xss[i + 1],
                range(len(xss) - 1), True)
            ans = reduce(lambda a, i: a and xss[i] <= xss[i + 1],
                range(len(xss) - 1), True)
            for fn1 in [seqops.is_ordered_i, seqops.is_ordered_r,
                    seqops.is_ordered_lp]:
                self.assertEqual(ansrev, fn1(xss, reverse=True))
                self.assertEqual(ans, fn1(xss))

    def test_sort(self):
        for xss in [['a', 'd', 'b', 'c'], ['c', 'b', 'a', 'e'], LST, REVLST]:
            ansrev, ans = sorted(xss, reverse=True), sorted(xss)
            for fn1 in [seqops.quick_sort]:
                lst_rev, lst = xss[:], xss[:]
                fn1(lst_rev, 0, len(xss) - 1, reverse=True)
                fn1(lst, 0, len(xss) - 1)
                self.assertEqual(ansrev, lst_rev)
                self.assertEqual(ans, lst)
                for fn_verify in [seqops.is_ordered_i, seqops.is_ordered_r,
                        seqops.is_ordered_lp]:
                    self.assertTrue(fn_verify(lst_rev, reverse=True))
                    self.assertTrue(fn_verify(lst))


    def test_append(self):
        lst2 = [9, 9, 9, 9]
        lst, revlst = seqops.copy_of_i(LST), seqops.copy_of_i(REVLST)
        for xss in [lst, revlst]:
            ans = (xss + lst2)
            for fn1 in [seqops.append_i, seqops.append_r, seqops.append_lp]:
                self.assertEqual(ans, fn1(xss, lst2))

    def test_interleave(self):
        lst2 = [9, 9, 9, 9]
        for fn1 in [seqops.interleave_i, seqops.interleave_r,
                seqops.interleave_lp]:
            self.assertEqual([0, 9, 1, 9, 2, 9, 3, 9, 4], fn1(LST, lst2))

    def test_map2(self):
        def proc(e1, e2): return e1 + e2 + 2
        for xss in [LST, REVLST]:
            ans = reduce(lambda a, i: a + [proc(xss[i], xss[i])],
                range(len(xss)), [])
            for fn1 in [seqops.map2_i, seqops.map2_r, seqops.map2_lp]:
                self.assertEqual(ans, fn1(proc, xss, xss))

    def test_zip(self):
        lst1, lst2 = [0, 1, 2], [20, 30, 40]
        ans = list(zip(lst1, lst2))
        for fn1 in [seqops.zip_i, seqops.zip_r, seqops.zip_lp]:
            self.assertEqual(ans, fn1(lst1, lst2))

    def test_unzip(self):
        lst = [(0, 20), (1, 30)]
        ans = list(zip(*lst))
        for fn1 in [seqops.unzip_i]:
            self.assertEqual(ans, fn1(lst))

    def test_concat(self):
        nlst1, nlst2 = [[0, 1, 2], [20, 30]], [[[0, 1]], [], [[20, 30]]]
        for nlst in [nlst1, nlst2]:
            ans = reduce(lambda a, e: a + e, nlst, [])
            for fn1 in [seqops.concat_i, seqops.concat_r, seqops.concat_lp]:
                self.assertEqual(ans, fn1(nlst))
