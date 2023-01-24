# -*- coding: utf-8 -*-
'''Classic hiorder module (variations using higher-order functions).

'''

from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import logging, inspect, operator
from functools import reduce
#from builtins import (ascii, filter, hex, map, oct, zip, range)

from intro_py import util


MODULE_LOGGER = logging.getLogger(__name__)

def unfold_right_i(func, seed):
    def iter(cur, acc):
        if func(cur) is None: return acc
        (a, new_seed) = func(cur)
        return iter(new_seed, [a] + acc)
    return iter(seed, [])

def unfold_left_r(func, seed):
    if func(seed) is None: return []
    (a, new_seed) = func(seed)
    return [a] + unfold_left_r(func, new_seed)


def expt_f(base, num):
    # return reduce(lambda a, e: base ** e, range(1, int(num) + 1), 1.0)
    return reduce(lambda a, e: a * base, range(1, int(num) + 1), 1.0)

def square_f(num): return expt_f(num, 2.0)

def numseq_math_f(op, hi, lo):
    init = 0 if op in [operator.add, operator.sub] else 1
    return reduce(op, range(lo, hi + 1), init)

def sum_to_f(hi, lo): return numseq_math_f(operator.add, hi, lo)

def fact_f(num): return numseq_math_f(operator.mul, num, 1)

def fib_f(num):
    return reduce(lambda s0_s1, e: (s0_s1[0] + s0_s1[1], s0_s1[0]),
        range(num), (0, 1))[0]

def pascaltri_f(rows):
    return reduce(lambda a, e: a + [list(map(operator.add, [0] + a[-1],
        a[-1] + [0]))], range(rows), [[1]])

def gcd_f(nums):
    import math
    return abs(reduce(math.gcd, nums[1:], nums[0]))

def lcm_f(nums):
    import math
    return abs(reduce(lambda a, e: a * int(e / math.gcd(a, e)), nums[1:],
        nums[0]))

def base_expand_f(base, num):
    import math
    return reduce(lambda a, e: (([a[1] % base] if 0 != a[1]
        else []) + a[0], a[1] // base),
        range(int(round(math.log(num, base))) + 1), ([], num))[0]

def base_to10_f(base, nums):
    return reduce(lambda a, i_e: a + (i_e[1] * int(base ** i_e[0])),
        enumerate(reversed(nums)), 0)

def range_step_f(step, start, stop):
    cmp_op = operator.gt if step > 0 else operator.lt
    if cmp_op(start, stop): return []
    return reduce(lambda a, e: a + ([e + step] if not cmp_op(a[-1], stop)
        else []), range(start, stop, step), [start])

def range_f(start, stop): return range_step_f(1, start, stop)


def expt_u(base, num):
    def ufunc(acc_cnt):
        if 1 > acc_cnt[1]: return None
        return (acc_cnt[0] * base, (acc_cnt[0] * base, acc_cnt[1] - 1))
    return util.head_or(0.0, unfold_right_i(ufunc, (1, num)))

def square_u(num): return expt_u(num, 2.0)

def numseq_math_u(op, hi, lo):
    init = 0 if op in [operator.add, operator.sub] else 1
    def ufunc(acc_cur):
        (acc, cur) = acc_cur
        return None if hi < cur else (op(acc, cur), (op(acc, cur), cur + 1))
    return util.head_or(init, unfold_right_i(ufunc, (init, lo)))

def sum_to_u(hi, lo): return numseq_math_u(operator.add, hi, lo)

def fact_u(num): return numseq_math_u(operator.mul, num, 1)

def fib_u(num):
    def ufunc(s0_s1_cnt):
        (s0, s1, cnt) = s0_s1_cnt
        return None if 0 > cnt else (s0, (s1, s0 + s1, cnt - 1))
    return util.head_or(0, unfold_right_i(ufunc, (0, 1, num)))

def pascaltri_u(rows):
    def ufunc(row_cnt):
        if 0 > row_cnt[1]: return None
        new_row = list(map(operator.add, [0] + row_cnt[0], row_cnt[0] + [0]))
        return (row_cnt[0], (new_row, row_cnt[1] - 1))
    #return list(reversed(unfold_right_i(ufunc, ([1], rows))))
    return unfold_left_r(ufunc, ([1], rows))

#def euclid_u(m, n):
#    def ufunc(a_b):
#        return None if 0 == a_b[1] else (a_b[1], (a_b[1], a_b[0] % a_b[1]))
#    return util.head_or(m, unfold_right_i(ufunc, (m, n)))

def gcd_u(nums):
    import math
    if [] == nums: return 0
    def ufunc(acc_rst):
        (acc, rst) = acc_rst
        if [] == rst: return None
        cur = math.gcd(acc, rst[0])
        return (cur, (cur, rst[1:]))
    return abs(util.head_or(nums[0], unfold_right_i(ufunc,
        (nums[0], nums[1:]))))

def lcm_u(nums):
    import math
    if [] == nums: return 0
    def ufunc(acc_rst):
        (acc, rst) = acc_rst
        if [] == rst: return None
        cur = acc * int(rst[0] / math.gcd(acc, rst[0]))
        return (cur, (cur, rst[1:]))
    return abs(util.head_or(nums[0], unfold_right_i(ufunc,
        (nums[0], nums[1:]))))

def base_expand_u(base, num):
    def ufunc(n):
        return None if 0 >= n else (n % base, n // base)
    return unfold_right_i(ufunc, num)

def base_to10_u(base, nums):
    def ufunc(acc_idx_rst):
        (acc, idx, rst) = acc_idx_rst
        if [] == rst: return None
        addon = rst[-1] * (base ** idx)
        return (acc + addon, (acc + addon, idx + 1, rst[:-1]))
    return util.head_or(0, unfold_right_i(ufunc, (0, 0, nums)))

def range_step_u(step, start, stop):
    cmp_op = operator.gt if step > 0 else operator.lt
    def ufunc(cur):
        return None if cmp_op(cur, stop) else (cur, cur + step)
    #return list(reversed(unfold_right_i(ufunc, start)))
    return unfold_left_r(ufunc, start)

def range_u(start, stop): return range_step_u(1, start, stop)


def expt_lc(base, num):
    # return ([1.0] + [base ** x for x in range(1, num + 1)])[-1]
    return ([0.0] + [x for x in [1.0] for i in range(1, int(num) + 1)
        for x in [x * base]])[-1]

def square_lc(num): return expt_lc(num, 2.0)

def numseq_math_lc(op, hi, lo):
    init = 0 if op in [operator.add, operator.sub] else 1
    return ([init] + [x for x in [init] for i in range(lo, hi + 1)
        for x in [op(x, i)]])[-1]

def sum_to_lc(hi, lo): return numseq_math_lc(operator.add, hi, lo)

def fact_lc(num): return numseq_math_lc(operator.mul, num, 1)

def fib_lc(num):
    return ([0] + [s0 for [s0, s1] in [[0, 1]] for i in range(num)
        for [s0, s1] in [[s1, s0 + s1]]])[-1]

def pascaltri_lc(rows):
    return [[1]] + [row for row in [[1]] for i in range(rows)
        for row in [list(map(operator.add, [0] + row, row + [0]))]]

def gcd_lc(nums):
    import math
    return abs(([nums[0]] + [x for x in [nums[0]] for n in nums[1:]
        for x in [math.gcd(x, n)]])[-1])

def lcm_lc(nums):
    import math
    return abs(([nums[0]] + [x for x in [nums[0]] for n in nums[1:]
        for x in [x * int(n / math.gcd(x, n))]])[-1])

def base_expand_lc(base, num):
    import math
    return list(reversed([x % base for x in [num * base]
        for i in range(int(round(math.log(num, base))) + 1)
        for x in [x // base] if 0 != x]))

def base_to10_lc(base, nums):
    return ([0] + [x for x in [0] for (i, e) in enumerate(reversed(nums))
        for x in [x + (e * int(base ** i))]])[-1]

def range_step_lc(step, start, stop):
    cmp_op = operator.gt if step > 0 else operator.lt
    if cmp_op(start, stop): return []
    return ([start] + [x for x in [0] for n in range(start, stop + step, step)
            for x in [n + step] if not cmp_op(x, stop)])

def range_lc(start, stop): return range_step_lc(1, start, stop)
