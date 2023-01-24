# -*- coding: utf-8 -*-
'''Test cases for Classic module.'''
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import unittest, operator
from functools import reduce
#from builtins import (ascii, filter, hex, map, oct, zip, range)

from intro_py import util
from intro_py.practice import classic

def setUpModule():
    '''Set up (module-level) test fixtures, if any.'''
    print('Setup module: {0}'.format(__name__))

def tearDownModule():
    '''Tear down (module-level) test fixtures, if any.'''
    print('Teardown module: {0}'.format(__name__))

class TestClassic(unittest.TestCase):
    '''Tests for Classic module.'''

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

    def test_square(self):
        for (num,) in util.bound_values(*[(2, 20)]):
            ans = num ** 2.0
            for fn1 in [classic.square_i, classic.square_r, classic.square_lp,
                    classic.square_f, classic.square_u, classic.square_lc]:
                self.assertEqual(ans, fn1(num))
            for res_gen in [classic.squares_mut_y(), classic.squares_y(),
                    classic.squares_map2y(), classic.squares_uy(),
                    classic.squares_ge()]:
                self.assertEqual(ans,
                    [next(res_gen) for i in range(num + 1)][-1])

    def test_sum_to(self):
        for hi, lo in [(hi, lo) for hi in [-15, 0, 150] for lo in [-20, 0, 10]]:
            ans = reduce(operator.add, range(lo, hi + 1), 0)
            for fn1 in [classic.sum_to_i, classic.sum_to_r, classic.sum_to_lp,
                    classic.sum_to_f, classic.sum_to_u, classic.sum_to_lc]:
                self.assertEqual(ans, fn1(hi, lo))
            for res_gen in [classic.sums_mut_y(lo), classic.sums_y(lo),
                    classic.sums_map2y(lo), classic.sums_uy(lo),
                    classic.sums_ge(lo)]:
                self.assertEqual(ans, 
                    ([0] + [next(res_gen) for i in range(lo, hi + 1)])[-1])

    def test_fact(self):
        # for num in [0, 9, 18]:
        for (num,) in util.bound_values(*[(0, 18)]):
            ans = (reduce(operator.mul, range(1, num + 1), 1))
            for fn1 in [classic.fact_i, classic.fact_r, classic.fact_lp,
                    classic.fact_f, classic.fact_u, classic.fact_lc]:
                self.assertEqual(ans, fn1(num))
            for res_gen in [classic.facts_mut_y(), classic.facts_y(),
                    classic.facts_map2y(), classic.facts_uy(),
                    classic.facts_ge()]:
                self.assertEqual(ans, 
                    [next(res_gen) for i in range(num + 1)][-1])
                self.assertEqual(ans * (num + 1), next(res_gen))

    def test_fib(self):
        for (num,) in util.bound_values(*[(0, 20)]):
            ans = reduce(lambda s0_s1, e: (s0_s1[0] + s0_s1[1], s0_s1[0]),
                range(num), (0, 1))[0]
            for fn1 in [classic.fib_i, classic.fib_r, classic.fib_lp,
                    classic.fib_f, classic.fib_u, classic.fib_lc]:
                self.assertEqual(ans, fn1(num))
            for res_gen in [classic.fibs_mut_y(), classic.fibs_y(),
                    classic.fibs_map2y(), classic.fibs_uy(), classic.fibs_ge()]:
                self.assertEqual(ans,
                    [next(res_gen) for i in range(num + 1)][-1])

    def test_expt(self):
        # for (base, num) in [(b, n) for b in [2.0, 11.0, 20.0]
        #    for n in [3.0, 6.0, 10.0]]:
        for (base, num) in util.bound_values(*[(2.0, 20.0), (3.0, 10.0)]):
            ans = base ** num
            for fn1 in [classic.expt_i, classic.expt_r, classic.expt_lp,
                    classic.fast_expt_i, classic.fast_expt_r,
                    classic.fast_expt_lp, classic.expt_f, classic.expt_u,
                    classic.expt_lc]:
                # self.assertEqual(ans, fn1(base, num))
                self.assertTrue(util.in_epsilon(ans, fn1(base, num),
                    0.001 * ans))
            for res_gen in [classic.expts_y(base), classic.expts_mut_y(base),
                    classic.expts_map2y(base), classic.expts_uy(base),
                    classic.expts_ge(base)]:
                res = [next(res_gen) for i in range(int(num + 1))][-1]
                #self.assertEqual(ans, res)
                self.assertTrue(util.in_epsilon(0.001 * ans, ans, res))

    def test_pascaltri(self):
        for (rows,) in util.bound_values(*[(0, 10)]):
            ans = reduce(lambda a, e: a + [list(map(operator.add, [0] + a[-1],
                a[-1] + [0]))], range(rows), [[1]])
            for fn1 in [classic.pascaltri_add, classic.pascaltri_mult,
                    classic.pascaltri_lp, classic.pascaltri_f,
                    classic.pascaltri_u, classic.pascaltri_lc]:
                self.assertEqual(ans, fn1(rows))
            for res_gen in [classic.pascalrows_y(), classic.pascalrows_mut_y(),
                    classic.pascalrows_map2y(), classic.pascalrows_uy(),
                    classic.pascalrows_ge()]:
                self.assertEqual(ans, [next(res_gen) for i in range(rows + 1)])

    def test_quot_rem(self):
        for num_a, num_b in [(a, b) for a in [10, -10] for b in [3, -3]]:
            self.assertEqual((num_a // num_b), classic.quot_m(num_a, num_b))
            self.assertEqual((num_a % num_b), classic.rem_m(num_a, num_b))

    def test_gcd_lcm(self):
        import math
        for nums in [[24, 16], [24, 16, 12], [24, 16, 32]]:
            ans_gcd = reduce(math.gcd, nums[1:], nums[0])
            ans_lcm = reduce(lambda a, e: a * int(e / math.gcd(a, e)),
                nums[1:], nums[0])
            for fn_gcd, fn_lcm in [(classic.gcd_i, classic.lcm_i),
                    (classic.gcd_r, classic.lcm_r),
                    (classic.gcd_lp, classic.lcm_lp),
					(classic.gcd_f, classic.lcm_f),
					(classic.gcd_u, classic.lcm_u),
					(classic.gcd_lc, classic.lcm_lc)]:
                self.assertEqual(ans_gcd, fn_gcd(nums))
                self.assertEqual(ans_lcm, fn_lcm(nums))

    def test_base_expand(self):
        import math
        for base, num in [(2, 11), (4, 81), (3, 243), (2, 16)]:
            ans = reduce(lambda a, e: (([a[1] % base] if 0 != a[1]
                else []) + a[0], a[1] // base),
                range(int(round(math.log(num, base))) + 1), ([], num))[0]
            for fn1 in [classic.base_expand_i, classic.base_expand_r,
                    classic.base_expand_lp, classic.base_expand_f,
					classic.base_expand_u, classic.base_expand_lc]:
                self.assertEqual(ans, fn1(base, num))

    def test_base_to10(self):
        for base, nums in [(2, [1, 0, 1, 1]), (4, [1, 1, 0, 1]),
                (3, [1, 0, 0, 0, 0, 0])]:
            ans = reduce(lambda a, i_e: a + (i_e[1] * int(base ** i_e[0])),
                enumerate(reversed(nums)), 0)
            for fn1 in [classic.base_to10_i, classic.base_to10_r,
                    classic.base_to10_lp, classic.base_to10_f,
					classic.base_to10_u, classic.base_to10_lc]:
                self.assertEqual(ans, fn1(base, nums))

    def test_range(self):
        LST, REVLST = list(range(0, 5)), list(range(4, -1, -1))
        for fn1, fnStep in [(classic.range_i, classic.range_step_i),
                (classic.range_r, classic.range_step_r),
                (classic.range_lp, classic.range_step_lp),
				(classic.range_f, classic.range_step_f),
				(classic.range_u, classic.range_step_u),
				(classic.range_lc, classic.range_step_lc)]:
            self.assertTrue(LST == fn1(0, 4) == fnStep(1, 0, 4))
            self.assertEqual(REVLST, fnStep(-1, 4, 0))
