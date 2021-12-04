# -*- coding: utf-8 -*-
'''Test properties for Sequenceops module.'''
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import unittest, operator, itertools
from functools import reduce
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

    @given(st.integers(min_value=0, max_value=10))
    def test_prop_tabulate(self, cnt):
        from itertools import count
        def proc_id(el): return el
        def proc1(el): return 16 * (2 ** el)
        for func, cnt in [(proc_id, cnt), (proc1, cnt)]:
            ans_gen = map(func, count())
            ans = [next(ans_gen) for i in range(cnt)]
            for fn1 in [seqops.tabulate_i, seqops.tabulate_r,
                    seqops.tabulate_lp, seqops.tabulate_f, seqops.tabulate_u,
                    seqops.tabulate_lc, seqops.tabulate_imap]:
                self.assertEqual(ans, fn1(func, cnt))

    @given(st.lists(st.integers(), max_size=20))
    def test_prop_length(self, xss):
        ans = len(xss)
        for fn1 in [seqops.length_i, seqops.length_r, seqops.length_lp,
                seqops.length_f, seqops.length_u, seqops.length_lc]:
            self.assertEqual(ans, fn1(xss))

    @given(st.data(), st.lists(st.integers(), min_size=1, max_size=20))
    def test_prop_nth(self, data, xss):
        ndx = data.draw(st.sampled_from(tuple(range(len(xss)))))
        ans = xss[ndx]
        for fn1 in [seqops.nth_i, seqops.nth_r, seqops.nth_lp, seqops.nth_f,
                seqops.nth_u, seqops.nth_lc, seqops.nth_islice]:
            self.assertEqual(ans, fn1(ndx, xss))

    @given(st.data(), st.lists(st.integers(), min_size=1, max_size=20))
    def test_prop_index(self, data, xss):
        data1 = data.draw(st.sampled_from(tuple(xss)))
        ans = xss.index(data1)
        for fn1 in [seqops.index_i, seqops.index_r, seqops.index_lp,
                seqops.index_f, seqops.index_u, seqops.index_lc]:
            self.assertEqual(ans, fn1(data1, xss))
            self.assertEqual(-1, fn1(-20, list(range(0, 20))))

    @given(st.data(), st.lists(st.integers(), min_size=1, max_size=20))
    def test_prop_find(self, data, xss):
        data1 = data.draw(st.sampled_from(tuple(xss)))
        for fn1 in [seqops.find_i, seqops.find_r, seqops.find_lp,
                seqops.find_f, seqops.find_u, seqops.find_lc]:
            self.assertEqual(data1, fn1(data1, xss))

    @given(st.lists(st.integers(), min_size=1, max_size=20))
    def test_prop_min_max(self, xss):
        ans_min, ans_max = min(xss), max(xss)
        for (fn_min, fn_max) in [(seqops.min_i, seqops.max_i),
                (seqops.min_r, seqops.max_r), (seqops.min_lp, seqops.max_lp),
                (seqops.min_f, seqops.max_f), (seqops.min_u, seqops.max_u),
                (seqops.min_lc, seqops.max_lc)]:
            self.assertEqual(ans_min, fn_min(xss))
            self.assertEqual(ans_max, fn_max(xss))

    @given(st.lists(st.integers(), max_size=20))
    def test_prop_reverse(self, xss):
        ans = list(reversed(xss[:]))
        for fn1 in [seqops.reverse_i, seqops.reverse_r, seqops.reverse_lp,
                seqops.reverse_f, seqops.reverse_u, seqops.reverse_lc]:
            self.assertEqual(ans, fn1(xss))

    @given(st.lists(st.integers(), max_size=20))
    def test_prop_reverse_mut(self, xss):
        exp_lst = xss[:]
        exp_lst.reverse()
        for fn1 in [seqops.reverse_mut_i, seqops.reverse_mut_lp]:
            act_lst = xss[:]
            fn1(act_lst)
            self.assertEqual(exp_lst, act_lst)

    @given(st.lists(st.integers(), max_size=20))
    def test_prop_copy_of(self, xss):
        ans = xss[:]
        for fn1 in [seqops.copy_of_i, seqops.copy_of_r, seqops.copy_of_lp,
                seqops.copy_of_f, seqops.copy_of_u, seqops.copy_of_lc]:
            self.assertEqual(ans, fn1(xss))

    @given(st.integers(min_value=0, max_value=25), st.lists(st.integers(),
        min_size=1, max_size=25))
    def test_prop_take_drop(self, int_n, xss):
        ans_take = reduce(lambda a, i_e: a + [i_e[1]] if int_n > i_e[0] else a,
            enumerate(xss), [])
        ans_drop = reduce(lambda a, i_e: a + [i_e[1]] if int_n <= i_e[0] else a,
            enumerate(xss), [])
        for (fn_take, fn_drop) in [(seqops.take_i, seqops.drop_i),
                (seqops.take_lp, seqops.drop_lp),
                (seqops.take_f, seqops.drop_f),
                (seqops.take_u, seqops.drop_u),
                (seqops.take_lc, seqops.drop_lc),
                (seqops.take_islice, seqops.drop_islice)]:
            self.assertEqual(ans_take, fn_take(int_n, xss))
            self.assertEqual(ans_drop, fn_drop(int_n, xss))
        for fn1 in [seqops.split_at_i, seqops.split_at_lp, seqops.split_at_f,
                seqops.split_at_u, seqops.split_at_lc, seqops.split_at_islice]:
            res = fn1(int_n, xss)
            self.assertEqual(ans_take, res[0])
            self.assertEqual(ans_drop, res[1])

    @given(st.lists(st.integers(), max_size=25))
    def test_prop_any_all(self, xss):
        def pred1(el): return 0 == el % 2
        ans_any = reduce(lambda a, e: a or pred1(e), xss, False)
        ans_all = reduce(lambda a, e: a and pred1(e), xss, True)
        for (fn_any, fn_all) in [(seqops.any_i, seqops.all_i),
                (seqops.any_r, seqops.all_r), (seqops.any_lp, seqops.all_lp),
                (seqops.any_f, seqops.all_f), (seqops.any_u, seqops.all_u),
                (seqops.any_lc, seqops.all_lc)]:
            self.assertEqual(ans_any, fn_any(pred1, xss))
            self.assertEqual(ans_all, fn_all(pred1, xss))

    @given(st.lists(st.integers(), max_size=20))
    def test_prop_map(self, xss):
        def proc(el): return el + 2
        ans = list(map(proc, xss))
        for fn1 in [seqops.map_i, seqops.map_r, seqops.map_lp, seqops.map_f,
                seqops.map_u, seqops.map_lc]:
            self.assertEqual(ans, fn1(proc, xss))

    @given(st.lists(st.integers(), max_size=20))
    def test_prop_foreach(self, xss):
        def proc(el): print('{0} '.format(el))
        ans = None
        for fn1 in [seqops.foreach_i, seqops.foreach_r, seqops.foreach_lp,
                seqops.foreach_f, seqops.foreach_u, seqops.foreach_lc]:
            self.assertEqual(ans, fn1(proc, xss))

    @given(st.lists(st.integers(), max_size=25))
    def test_prop_filter_remove(self, xss):
        def pred1(el): return 0 == el % 2
        ans_filter = reduce(lambda a, e: a + [e] if pred1(e) else a, xss, [])
        ans_remove = reduce(lambda a, e: a + [e] if not pred1(e) else a, xss, [])
        for (fn_f, fn_r) in [(seqops.filter_i, seqops.remove_i),
                (seqops.filter_r, seqops.remove_r),
                (seqops.filter_lp, seqops.remove_lp),
                (seqops.filter_f, seqops.remove_f),
                (seqops.filter_u, seqops.remove_u),
                (seqops.filter_lc, seqops.remove_lc)]:
            self.assertEqual(ans_filter, fn_f(pred1, xss))
            self.assertEqual(ans_remove, fn_r(pred1, xss))
        for fn1 in [seqops.partition_i, seqops.partition_r,
                seqops.partition_lp, seqops.partition_f,
                seqops.partition_u, seqops.partition_lc]:
            res = fn1(pred1, xss)
            self.assertEqual(ans_filter, res[0])
            self.assertEqual(ans_remove, res[1])

    @given(st.lists(st.integers(), max_size=25))
    def test_prop_fold_left(self, xss):
        def corp(acc, el): return acc + el
        ans = reduce(corp, xss, 0)
        for fn1 in [seqops.fold_left_i, seqops.fold_left_r, seqops.fold_left_lp]:
            self.assertEqual(ans, fn1(corp, 0, xss))

    @given(st.lists(st.integers(), max_size=25))
    def test_prop_fold_right(self, xss):
        def proc(e, a): return e - a
        ans = reduce(lambda a, e: proc(e, a), reversed(xss), 0)
        for fn1 in [seqops.fold_right_i, seqops.fold_right_r,
                seqops.fold_right_lp]:
            self.assertEqual(ans, fn1(proc, xss, 0))

    @given(st.integers(min_value=0, max_value=25))
    def test_prop_unfold_range(self, num):
        ans = list(range(num + 1))
        def ufunc(cur):
            if num < cur: return None
            return (cur, cur + 1)
        for fn1 in [seqops.unfold_right_i, seqops.unfold_right_lp]:
            self.assertEqual(ans, list(reversed(fn1(ufunc, 0))))
        for fn1 in [seqops.unfold_left_r, seqops.unfold_left_lp]:
            self.assertEqual(ans, fn1(ufunc, 0))

    @given(st.integers(min_value=0, max_value=25))
    def test_prop_unfold_fib(self, num):
        ans = reduce(lambda s0_s1, e: (s0_s1[0] + s0_s1[1], s0_s1[0]),
            range(num), (0, 1))[0]
        def ufunc(s0_s1_cnt):
            (s0, s1, cnt) = s0_s1_cnt
            if 0 > cnt: return None
            return (s0, (s1, s0 + s1, cnt - 1))
        for fn1 in [seqops.unfold_right_i, seqops.unfold_right_lp]:
            self.assertEqual(ans, fn1(ufunc, (0, 1, num))[0])
        for fn1 in [seqops.unfold_left_r, seqops.unfold_left_lp]:
            self.assertEqual(ans, fn1(ufunc, (0, 1, num))[-1])

    @given(st.data())
    def test_prop_unfold_base_to10(self, data):
        base = data.draw(st.sampled_from(tuple(range(2, 17))))
        nums_len = data.draw(st.sampled_from(tuple(range(1, 19))))
        nums = [data.draw(st.sampled_from(tuple(range(base)))) for i in range(nums_len)]
        ans = reduce(lambda a, i_e: a + (i_e[1] * int(base ** i_e[0])),
            enumerate(reversed(nums)), 0)
        def ufunc(acc_idx_rst):
            (acc, idx, rst) = acc_idx_rst
            if [] == rst: return None
            addon = rst[-1] * (base ** idx)
            return (acc + addon, (acc + addon, idx + 1, rst[:-1]))
        for fn1 in [seqops.unfold_right_i, seqops.unfold_right_lp]:
            self.assertEqual(ans, fn1(ufunc, (0, 0, nums))[0])
        for fn1 in [seqops.unfold_left_r, seqops.unfold_left_lp]:
            self.assertEqual(ans, fn1(ufunc, (0, 0, nums))[-1])

    @given(st.data())
    def test_prop_unfold_unsum(self, data):
        ans = data.draw(st.sampled_from(tuple(range(26))))
        prob = reduce(operator.add, range(1, ans + 1), 0)
        def ufunc(fst_snd):
            (fst, snd) = fst_snd
            if 0 >= snd: return None
            return (fst, (fst + 1, snd - fst))
        for fn1 in [seqops.unfold_right_i, seqops.unfold_right_lp]:
            self.assertEqual(ans, (fn1(ufunc, (0, prob)) + [0])[0])
        for fn1 in [seqops.unfold_left_r, seqops.unfold_left_lp]:
            self.assertEqual(ans, ([0] + fn1(ufunc, (0, prob)))[-1])

    @given(st.data())
    def test_prop_unfold_unproduct(self, data):
        ans = data.draw(st.sampled_from(tuple(range(1, 26))))
        prob = reduce(operator.mul, range(1, ans + 1), 1)
        def ufunc(fst_snd):
            (fst, snd) = fst_snd
            if 1 >= snd: return None
            return (fst, (fst + 1, snd / fst))
        for fn1 in [seqops.unfold_right_i, seqops.unfold_right_lp]:
            self.assertEqual(ans, (fn1(ufunc, (1, prob)) + [1])[0])
        for fn1 in [seqops.unfold_left_r, seqops.unfold_left_lp]:
            self.assertEqual(ans, ([1] + fn1(ufunc, (1, prob)))[-1])


    @given(st.lists(st.integers(), min_size=2, max_size=25))
    def test_prop_is_ordered(self, xss):
        yss = sorted(xss)
        ans = reduce(lambda a, i: a and xss[i] <= xss[i + 1],
            range(len(xss) - 1), True)
        ans_sorted = reduce(lambda a, i: a and yss[i] <= yss[i + 1],
            range(len(yss) - 1), True)
        for fn1 in [seqops.is_ordered_i, seqops.is_ordered_r,
                seqops.is_ordered_lp, seqops.is_ordered_f,
                seqops.is_ordered_lc, seqops.is_ordered_u]:
            self.assertEqual(ans, fn1(xss))
            self.assertEqual(ans_sorted, fn1(yss))

    @given(st.lists(st.integers(), min_size=2, max_size=25))
    def test_prop_sort(self, xss):
        ans = sorted(xss)
        ansrev = sorted(xss, reverse=True)
        for fn1 in [seqops.quick_sort]:
            lst_rev, lst = xss[:], xss[:]
            fn1(lst_rev, 0, len(xss) - 1, reverse=True)
            fn1(lst, 0, len(xss) - 1)
            self.assertEqual(ans, lst)
            self.assertEqual(ansrev, lst_rev)
            for fn_verify in [seqops.is_ordered_i, seqops.is_ordered_r,
                    seqops.is_ordered_lp, seqops.is_ordered_f,
                    seqops.is_ordered_lc, seqops.is_ordered_u]:
                self.assertTrue(fn_verify(lst_rev, reverse=True))
                self.assertTrue(fn_verify(lst))


    @given(st.lists(st.integers(), max_size=20), st.lists(st.integers(),
        max_size=20))
    def test_prop_append(self, xss, yss):
        ans = xss[:] + yss[:]
        for fn1 in [seqops.append_i, seqops.append_r, seqops.append_lp,
                seqops.append_f, seqops.append_u, seqops.append_lc]:
            self.assertEqual(ans, fn1(xss, yss))

    @given(st.lists(st.integers(), max_size=20), st.lists(st.integers(),
        max_size=20))
    def test_prop_interleave(self, xss, yss):
        len_short = len(xss) if len(xss) < len(yss) else len(yss)
        ans = (reduce(lambda wss_acc, y: (wss_acc[0][:-1],
            [wss_acc[0][-1], y] + wss_acc[1]),
            reversed(yss[:len_short]), (xss[:len_short], xss[len_short:] +
            yss[len_short:])))[1]
        for fn1 in [seqops.interleave_i, seqops.interleave_r,
                seqops.interleave_lp, seqops.interleave_f,
                seqops.interleave_u, seqops.interleave_lc]:
            self.assertEqual(ans, fn1(xss, yss))

    @given(st.lists(st.integers(), min_size=1, max_size=20),
        st.lists(st.integers(), min_size=1, max_size=20))
    def test_prop_map2(self, xss, yss):
        def proc(e1, e2): return e1 + e2 + 2
        len_short = len(xss) if len(xss) < len(yss) else len(yss)
        ans = reduce(lambda a, i: a + [proc(xss[i], yss[i])],
            range(len_short), [])
        for fn1 in [seqops.map2_i, seqops.map2_r, seqops.map2_lp,
                seqops.map2_f, seqops.map2_u, seqops.map2_lc]:
            self.assertEqual(ans, fn1(proc, xss, yss))

    @given(st.lists(st.integers(), min_size=1, max_size=20),
        st.lists(st.integers(), min_size=1, max_size=20))
    def test_prop_zip(self, xss, yss):
        ans = list(zip(xss, yss))
        for fn1 in [seqops.zip_i, seqops.zip_r, seqops.zip_lp,
                seqops.zip_f, seqops.zip_u, seqops.zip_lc]:
            self.assertEqual(ans, fn1(xss, yss))

    @given(st.lists(st.tuples(st.integers(), st.integers()), min_size=1,
        max_size=20))
    def test_prop_unzip(self, ziplst):
        ans = list(zip(*ziplst))
        for fn1 in [seqops.unzip_i, seqops.unzip_f, seqops.unzip_u,
                seqops.unzip_lc]:
            self.assertEqual(ans, fn1(ziplst))

    @given(st.lists(st.lists(st.integers(), max_size=20), max_size=20))
    def test_prop_concat(self, nlst):
        ans = reduce(lambda a, e: a + e, nlst, [])
        for fn1 in [seqops.concat_i, seqops.concat_r, seqops.concat_lp,
                seqops.concat_f, seqops.concat_u, seqops.concat_lc,
                seqops.concat_chain]:
            self.assertEqual(ans, fn1(nlst))
    
    
    @given(st.lists(st.integers(), max_size=20), st.lists(st.integers(),
        max_size=20), st.lists(st.integers(), max_size=20))
    def test_prop_any_all_v(self, xss, yss, zss):
        def pred1(el1): 0 == el1 % 2
        for lst in [[xss, yss], [xss, yss, zss]]:
            ans_any = any(map(pred1, itertools.chain(*lst)))
            ans_all = all(map(pred1, itertools.chain(*lst)))
            for (fn_any, fn_all) in [(seqops.any_lpv, seqops.all_lpv),
                    (seqops.any_fv, seqops.all_fv),
                    (seqops.any_lcv, seqops.all_lcv)]:
                self.assertEqual(ans_any, fn_any(pred1, *lst))
                self.assertEqual(ans_all, fn_all(pred1, *lst))
            for (anyGen, allGen) in [(seqops.any_yv, seqops.all_yv)]:
                #res_genAny = anyGen(pred1, *lst)
                #res_genAll = anyGen(pred1, *lst)
                #self.assertEqual(ans_any, [next(res_genAny) for i in
                #    range(len(list(zip(*lst))))][-1])
                #self.assertEqual(ans_all, [next(res_genAll) for i in
                #    range(len(list(zip(*lst))))][-1])
                resAny, resAll = list(anyGen(pred1, *lst)), list(allGen(pred1, *lst))
                self.assertEqual(ans_any, (False if [] == resAny else resAny[-1]))
                self.assertEqual(ans_all, (True if [] == resAll else resAll[-1]))

    @given(st.lists(st.integers(), max_size=20), st.lists(st.integers(),
        max_size=20), st.lists(st.integers(), max_size=20))
    def test_prop_map_v(self, xss, yss, zss):
        def proc2(el1, el2): return [el1 + 2, el2 + 2]
        def proc3(el1, el2, el3): return [el1 + 2, el2 + 2, el3 + 2]
        for proc, lst in [(proc2, [xss, yss]), (proc3, [xss, yss, zss])]:
            ans = list(map(proc, *lst))
            for fn1 in [seqops.map_lpv, seqops.map_yv, seqops.map_fv,
                    seqops.map_lcv]:
                self.assertEqual(ans, list(fn1(proc, *lst)))

    @given(st.lists(st.integers(), max_size=20), st.lists(st.integers(),
        max_size=20), st.lists(st.integers(), max_size=20))
    def test_prop_foreach_v(self, xss, yss, zss):
        def proc2(el1, el2): print(el1, el2)
        def proc3(el1, el2, el3): print(el1, el2, el3)
        for proc, lst in [(proc2, [xss, yss]), (proc3, [xss, yss, zss])]:
            ans = list(map(proc, *lst))
            for fn1 in [seqops.foreach_lpv, seqops.foreach_yv,
                    seqops.foreach_fv, seqops.foreach_lcv]:
                self.assertEqual(ans, list(fn1(proc, *lst)))

    @given(st.lists(st.integers(), max_size=20), st.lists(st.integers(),
        max_size=20), st.lists(st.integers(), max_size=20))
    def test_prop_fold_left_v(self, xss, yss, zss):
        def corp2(acc, el1, el2): return (acc + el1) + el2
        def corp3(acc, el1, el2, el3): return ((acc - el1) - el2) - el3
        for corp, lst in [(corp2, [xss, yss]), (corp3, [xss, yss, zss])]:
            ans = reduce(lambda a, e: corp(a, *e), list(zip(*lst)), 0)
            for fn1 in [seqops.fold_left_lpv]:
                self.assertEqual(ans, fn1(corp, 0, *lst))
            for fnGen in [seqops.fold_left_yv]:
                #res_gen = fnGen(corp, 0, *lst)
                #self.assertEqual(ans, ([0] + [next(res_gen) for i in
                #    range(len(list(zip(*lst))))])[-1])
                self.assertEqual(ans, ([0] + list(fnGen(corp, 0, *lst)))[-1])

    @given(st.lists(st.integers(), max_size=20), st.lists(st.integers(),
        max_size=20), st.lists(st.integers(), max_size=20))
    def test_prop_fold_right_v(self, xss, yss, zss):
        def proc2(acc, el1, el2): return (el1 + el2) + acc
        def proc3(acc, el1, el2, el3): return ((el1 + el2) + el3) - acc
        for proc, lst in [(proc2, [xss, yss]), (proc3, [xss, yss, zss])]:
            ans = reduce(lambda a, e: proc(a, *e), list(zip(*list(map(reversed,
                lst)))), 0)
            for fn1 in [seqops.fold_right_lpv]:
                self.assertEqual(ans, fn1(proc, 0, *lst))
            for fnGen in [seqops.fold_right_yv]:
                #res_gen = fnGen(proc, 0, *lst)
                #self.assertEqual(ans, ([0] + [next(res_gen) for i in
                #    range(len(list(zip(*lst))))])[-1])
                self.assertEqual(ans, ([0] + list(fnGen(proc, 0, *lst)))[-1])

    @given(st.lists(st.integers(), max_size=20), st.lists(st.integers(),
        max_size=20), st.lists(st.integers(), max_size=20))
    def test_prop_append_v(self, xss, yss, zss):
        for lst in [[xss, yss], [xss, yss, zss]]:
            ans = list(itertools.chain(*lst))
            for fn1 in [seqops.append_lpv, seqops.append_fv, seqops.append_lcv]:
                self.assertEqual(ans, fn1(*lst))
            for fn1 in [seqops.append_yv]:
                self.assertEqual(ans, list(fn1(*lst))[-1])

    @given(st.lists(st.integers(), max_size=20), st.lists(st.floats(),
        max_size=20), st.lists(st.characters(), max_size=20),
        st.lists(st.integers(), max_size=20))
    def test_prop_zip_v(self, xss, yss, zss, wss):
        for lst in [[xss, yss, zss], [xss, yss, zss, wss]]:
            ans = list(zip(*lst))
            for fn1 in [seqops.zip_lpv, seqops.zip_yv, seqops.zip_fv,
                    seqops.zip_lcv]:
                self.assertEqual(ans, list(fn1(*lst)))
