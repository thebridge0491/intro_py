# -*- coding: utf-8 -*-
'''Test properties for Classic module.'''
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import unittest , operator
from functools import reduce
from future.builtins import (ascii, filter, hex, map, oct, zip, object, str,
    range)

from intro_py import util
from intro_py.practice import classic

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

class TestPropsClassic(unittest.TestCase):
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

    @given(st.integers(min_value=0, max_value=100))
    def test_prop_square(self, int_n):
        ans = int_n ** 2.0
        for fn1 in [classic.square_i, classic.square_r, classic.square_lp]:
            self.assertEqual(ans, fn1(int_n))

    @given(st.integers(min_value=-50, max_value=150), st.integers(min_value=-50,
        max_value=150))
    def test_prop_sum_to(self, hi, lo):
        ans = reduce(operator.add, range(lo, hi + 1), 0)
        for fn1 in [f for f in [classic.sum_to_i, classic.sum_to_r,
                classic.sum_to_lp]]:
            self.assertEqual(ans, fn1(hi, lo))

    @given(st.integers(min_value=0, max_value=18))
    def test_prop_fact(self, num):
        ans = (reduce(operator.mul, range(1, num + 1), 1))
        for fn1 in [classic.fact_i, classic.fact_r, classic.fact_lp]:
            self.assertEqual(ans, fn1(num))

    @given(st.integers(min_value=0, max_value=20))
    def test_prop_fib(self, num):
        ans = reduce(lambda s0_s1, e: (s0_s1[0] + s0_s1[1], s0_s1[0]),
            range(num), (0, 1))[0]
        for fn1 in [classic.fib_i, classic.fib_r, classic.fib_lp]:
            self.assertEqual(ans, fn1(num))

    @given(st.integers(min_value=1, max_value=20), st.integers(min_value=2,
        max_value=10))
    def test_prop_expt(self, int_b, int_n):
        base, num = float(int_b), float(int_n)
        ans = base ** num
        for fn1 in [classic.expt_i, classic.expt_r, classic.expt_lp,
                classic.fast_expt_i, classic.fast_expt_r, classic.fast_expt_lp]:
            # self.assertEqual(ans, fn1(base, num))
            self.assertTrue(util.in_epsilon(ans, fn1(base, num),
                0.001 * ans))

    @given(st.integers(min_value=0, max_value=15))
    def test_prop_pascaltri(self, rows):
        ans = reduce(lambda a, e: a + [list(map(operator.add, [0] + a[-1],
            a[-1] + [0]))], range(rows), [[1]])
        for fn1 in [classic.pascaltri_add, classic.pascaltri_mult,
                classic.pascaltri_lp]:
            res = fn1(rows)
            self.assertEqual(ans, res)
            self.assertEqual(len(res), rows + 1)
            for idx, row in enumerate(res):
                self.assertEqual(len(row), idx + 1)
                self.assertEqual(reduce(operator.add, row, 0), int(2 ** idx))

    @given(st.integers(min_value=-50, max_value=150), st.integers(min_value=1,
        max_value=150))
    def test_prop_quot_rem(self, num_m, num_n):
        self.assertEqual((num_m // num_n), classic.quot_m(num_m, num_n))
        self.assertEqual((num_m % num_n), classic.rem_m(num_m, num_n))

    @given(st.lists(st.integers(min_value=1, max_value=500), min_size=1,
        max_size=19), st.lists(st.integers(min_value=-500, max_value=-1),
        min_size=1, max_size=19))
    def test_prop_gcd_lcm(self, lst_pos, lst_neg):
        import fractions
        ans_gcd_pos = reduce(fractions.gcd, lst_pos, 0)
        ans_lcm_pos = reduce(lambda a, e: a * int(e / fractions.gcd(a, e)),
            lst_pos[1:], lst_pos[0])
        for fn_gcd, fn_lcm in [(classic.gcd_i, classic.lcm_i),
                (classic.gcd_r, classic.lcm_r), (classic.gcd_lp, classic.lcm_lp)]:
            self.assertEqual(ans_gcd_pos, fn_gcd(lst_pos))
            self.assertEqual(ans_lcm_pos, fn_lcm(lst_pos))
        ans_gcd_neg = reduce(fractions.gcd, lst_neg, 0)
        ans_lcm_neg = reduce(lambda a, e: a * int(e / fractions.gcd(a, e)),
            lst_neg[1:], lst_neg[0])
        for fn_gcd, fn_lcm in [(classic.gcd_i, classic.lcm_i),
                (classic.gcd_r, classic.lcm_r), (classic.gcd_lp, classic.lcm_lp)]:
            self.assertEqual(ans_gcd_neg, fn_gcd(lst_neg))
            self.assertEqual(ans_lcm_neg, fn_lcm(lst_neg))

    @given(st.integers(min_value=2, max_value=17),
        st.integers(min_value=1, max_value=500))
    def test_prop_base_expand(self, base, num):
        import math
        ans = reduce(lambda a, e: (([a[1] % base] if 0 != a[1] else []) + a[0],
            a[1] // base), range(int(round(math.log(num, base))) + 1), ([], num))[0]
        for fn1 in [classic.base_expand_i, classic.base_expand_r,
                classic.base_expand_lp]:
            self.assertEqual(ans, fn1(base, num))

    @given(st.data())
    def test_prop_base_to10(self, data):
        base = data.draw(st.sampled_from(tuple(range(2, 17))))
        nums_len = data.draw(st.sampled_from(tuple(range(1, 19))))
        nums = [data.draw(st.sampled_from(tuple(range(base)))) for i in range(nums_len)]
        ans = reduce(lambda a, i_e: a + (i_e[1] * int(base ** i_e[0])),
            enumerate(reversed(nums)), 0)
        for fn1 in [classic.base_to10_i, classic.base_to10_r,
                classic.base_to10_lp]:
            self.assertEqual(ans, fn1(base, nums))

    @given(st.integers(min_value=-50, max_value=150), st.integers(min_value=-50,
        max_value=150))
    def test_prop_range(self, hi, lo):
        lst, revlst = list(range(lo, hi + 1)), list(range(hi, lo - 1, -1))
        for fn1, fnStep in [(classic.range_i, classic.range_step_i),
                (classic.range_r, classic.range_step_r),
                (classic.range_lp, classic.range_step_lp)]:
            self.assertTrue(lst == fn1(lo, hi) == fnStep(1, lo, hi))
            self.assertEqual(revlst, fnStep(-1, hi, lo))
