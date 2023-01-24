# -*- coding: utf-8 -*-
'''Classic module

'''

from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import sys, logging, inspect, operator
#from builtins import (ascii, filter, hex, map, oct, zip, range)

from .classic_puzzles import hanoi, nqueens, hanoi_moves, nqueens_grid
from .classic_hiorder import (square_f, sum_to_f, fact_f, fib_f, expt_f,
    pascaltri_f, gcd_f, lcm_f, base_expand_f, base_to10_f, range_step_f,
    range_f,
    
    square_u, sum_to_u, fact_u, fib_u, expt_u, pascaltri_u, gcd_u, lcm_u,
    base_expand_u, base_to10_u, range_step_u, range_u,
    
    square_lc, sum_to_lc, fact_lc, fib_lc, expt_lc, pascaltri_lc, gcd_lc,
    lcm_lc, base_expand_lc, base_to10_lc, range_step_lc, range_lc
)
from .classic_streams import (squares_mut_y, expts_mut_y, sums_mut_y,
    facts_mut_y, fibs_mut_y, pascalrows_mut_y,
    squares_y, expts_y, sums_y, facts_y, fibs_y, pascalrows_y,
    
    squares_map2y, expts_map2y, sums_map2y, facts_map2y, fibs_map2y,
    pascalrows_map2y,
    
    squares_uy, expts_uy, sums_uy, facts_uy, fibs_uy, pascalrows_uy,

    squares_ge, expts_ge, sums_ge, facts_ge, fibs_ge, pascalrows_ge
    )

__all__ = ['square_i', 'square_r', 'square_lp', 'sum_to_i', 'sum_to_r',
    'sum_to_lp', 'fact_i', 'fact_r', 'fact_lp', 'fib_i', 'fib_r', 'fib_lp',
    'expt_i', 'expt_r', 'expt_lp', 'fast_expt_i', 'fast_expt_r',
    'fast_expt_lp', 'pascaltri_add', 'pascaltri_mult', 'pascaltri_lp',
    'quot_m', 'rem_m', 'euclid_i', 'euclid_r', 'euclid_lp', 'gcd_i', 'gcd_r',
    'gcd_lp', 'lcm_i', 'lcm_r', 'lcm_lp', 'base_expand_i', 'base_expand_r',
    'base_expand_lp', 'base_to10_i', 'base_to10_r', 'base_to10_lp',
    'range_step_i', 'range_step_r', 'range_step_lp', 'range_i',
    'range_r', 'range_lp',

    'hanoi', 'hanoi_moves', 'nqueens', 'nqueens_grid',

    'square_f', 'sum_to_f', 'fact_f', 'fib_f', 'expt_f', 'pascaltri_f',
    'gcd_f', 'lcm_f', 'base_expand_f', 'base_to10_f', 'range_step_f',
    'range_f'

    'square_u', 'sum_to_u', 'fact_u', 'fib_u', 'expt_u', 'pascaltri_u',
    'gcd_u', 'lcm_u', 'base_expand_u', 'base_to10_u', 'range_step_u',
    'range_u'
    
    'square_lc', 'sum_to_lc', 'fact_lc', 'fib_lc', 'expt_lc', 'pascaltri_lc',
    'gcd_lc', 'lcm_lc', 'base_expand_lc', 'base_to10_lc', 'range_step_lc',
    'range_lc',
    
    'squares_mut_y', 'expts_mut_y', 'sums_mut_y', 'facts_mut_y', 'fibs_mut_y',
    'pascalrows_mut_y',
    'squares_y', 'expts_y', 'sums_y', 'facts_y', 'fibs_y', 'pascalrows_y',
    
    'squares_map2y', 'expts_map2y', 'sums_map2y', 'facts_map2y', 'fibs_map2y',
    'pascalrows_map2y',
    
    'squares_uy', 'expts_uy', 'sums_uy', 'facts_uy', 'fibs_uy',
    'pascalrows_uy',
    
    'squares_ge', 'expts_ge', 'sums_ge', 'facts_ge', 'fibs_ge',
    'pascalrows_ge'
    ]


MODULE_LOGGER = logging.getLogger(__name__)

def expt_i(base, num):
    def iter(cnt, acc):
        return acc if 0 >= cnt else iter(cnt - 1, base * acc)
    return iter(int(num), 1.0)

def square_i(num): return expt_i(num, 2.0)

def expt_r(base, num):
    return 1.0 if 0 >= num else base * expt_r(base, num - 1)

def square_r(num): return expt_r(num, 2.0)

def expt_lp(base, num):
    acc = 1.0
    for i in range(0, int(num)):
        acc *= base
    return acc

def square_lp(num): return expt_lp(num, 2.0)

def fast_expt_i(base, num):
    def iter(cnt, acc):
        if 0 >= cnt: return acc
        elif 0 == cnt % 2: return iter(cnt - 2, acc * (base ** 2.0))
        else: return iter(cnt - 1, acc * base)
    return iter(int(num), 1.0)

def fast_expt_r(base, num):
    if 0 >= num: return 1.0
    elif 0 == int(num) % 2: return fast_expt_r(base, num / 2) ** 2.0
    else: return base * fast_expt_r(base, num - 1)

def fast_expt_lp(base, num):
    acc, n = 1.0, num
    while n > 0.0:
        if 0 == n % 2:
            acc *= base * base
            n -= 2.0
        else:
            acc *= base
            n -= 1.0
    return acc

def numseq_math_i(op, hi, lo):
    init = 0 if op in [operator.add, operator.sub] else 1
    def iter(start, acc):
        return acc if start < lo else iter(start - 1, op(acc, start))
    return iter(hi, init)

def sum_to_i(hi, lo): return numseq_math_i(operator.add, hi, lo)

def fact_i(num):
    func_name = inspect.stack()[0][3]
    MODULE_LOGGER.info(func_name + '()')
    #
    return numseq_math_i(operator.mul, num, 1)

def numseq_math_r(op, hi, lo):
    init = 0 if op in [operator.add, operator.sub] else 1
    return init if hi < lo else op(hi, numseq_math_r(op, hi - 1, lo))

def sum_to_r(hi, lo): return numseq_math_r(operator.add, hi, lo)

def fact_r(num): return numseq_math_r(operator.mul, num, 1)

def numseq_math_lp(op, hi, lo):
    init = 0 if op in [operator.add, operator.sub] else 1
    acc = init
    # for i in range(hi, lo - 1, -1):
    for i in range(lo, hi + 1):
        acc = op(acc, i)
    return acc

def sum_to_lp(hi, lo): return numseq_math_lp(operator.add, hi, lo)

def fact_lp(num): return numseq_math_lp(operator.mul, num, 1)

def fib_i(num):
    def iter(s0, s1, cnt):
        return s0 if 0 >= cnt else iter(s1, s0 + s1, cnt - 1)
    return iter(0, 1, num)

def fib_r(num): return num if 2 > num else fib_r(num - 2) + fib_r(num - 1)

def fib_lp(num):
    s0, s1, acc = 0, 1, 0
    for i in range(0, num + 1):
        acc = s0
        s0 = s1
        s1 = s1 + acc
    return acc

def pascaltri_add(rows):
    def triangle(xss, num_rows):
        if 0 == num_rows: return []
        else:
            return [xss] + triangle(list(map(operator.add, [0] + xss,
                xss + [0])), num_rows - 1)
    return triangle([1], rows + 1)

def pascaltri_mult(rows):
    def pascalrow(r):
        def iter(col, xss):
            if [] == xss: raise Exception('empty list')
            elif r == col: return xss
            else: return iter(col + 1, [int(xss[0] * (r - col) / col)] + xss)
        return iter(1, [1])
    return list(map(pascalrow, range(1, rows + 2)))

def pascaltri_lp(rows):
    acc = [[1]]
    for row in range(1, rows + 1):
        acc += [[-1] * (row + 1)]
        acc[row][0] = acc[row][row] = 1
        for col in range(1, row):
            acc[row][col] = acc[row - 1][col - 1] + acc[row - 1][col]
    return acc

def quot_rem(num_a, num_b):
    q = num_a // num_b
    return (q, num_a - (q * num_b))

def quot_m(num_a, num_b): return quot_rem(num_a, num_b)[0]

def rem_m(num_a, num_b): return quot_rem(num_a, num_b)[1]

def euclid_i(num_m, num_n):
    def iter(a, b):
        return a if 0 == b else iter(b, a % b)
    return abs(iter(num_m, num_n))

def euclid_r(num_m, num_n):
    return abs(num_m) if 0 == num_n else abs(euclid_r(num_n, num_m % num_n))

def euclid_lp(num_m, num_n):
    acc, b, swap = num_m, num_n, 0
    while b != 0:
        swap = acc
        acc = b
        b = swap % b
    return abs(acc)

def gcd_i(nums):
    def iter(acc, rst):
        return acc if [] == rst else iter(euclid_i(acc, rst[0]), rst[1:])
    return abs(iter(nums[0], nums[1:]))

def gcd_r(nums):
    return (abs(nums[0]) if 1 == len(nums) else 
        gcd_r([euclid_r(nums[0], nums[1])] + nums[2:]))

def gcd_lp(nums):
    acc = nums[0]
    for i in range(1, len(nums)):
        acc = euclid_lp(acc, nums[i])
    return abs(acc)

def lcm_i(nums):
    def iter(acc, rst):
        if [] == rst: return acc
        else:
            n = rst[0]
            return iter(acc * int(n / euclid_i(acc, n)), rst[1:])
    return abs(iter(nums[0], nums[1:]))

def lcm_r(nums):
    if 1 == len(nums): return abs(nums[0])
    else:
        m, n = nums[0], nums[1]
        return lcm_r([m * int(n / euclid_r(m, n))] + nums[2:])

def lcm_lp(nums):
    acc = nums[0]
    for i in range(1, len(nums)):
        acc = acc * int(nums[i] / euclid_lp(acc, nums[i]))
    return abs(acc)

def base_expand_i(base, num):
    def iter(q, acc):
        return acc if 0 >= q else iter(q // base, [q % base] + acc)
    return iter(num, [])

def base_expand_r(base, num):
    return [] if 0 >= num else base_expand_r(base, num // base) + [num % base]

def base_expand_lp(base, num):
    acc, n = [], num
    while n > 0:
        acc = [n % base] + acc
        n = n // base
    return acc

def base_to10_i(base, nums):
    def iter(rst, idx, acc):
        if [] == rst: return acc
        else:
            n = rst[0]
            return iter(rst[1:], idx + 1, acc + (n * int(base ** idx)))
    return iter(list(reversed(nums)), 0, 0)

def base_to10_r(base, nums):
    if 1 == len(nums): return nums[0]
    return base_to10_r(base, nums[1:]) + (nums[0] * int(base ** len(nums[1:])))

def base_to10_lp(base, nums):
    acc, idx = 0, 0
    for i in range(len(nums) - 1, -1, -1):
        acc += nums[i] * int(base ** idx)
        idx += 1
    return acc

def range_step_i(step, start, stop):
    cmp_op = operator.gt if step > 0 else operator.lt
    #
    def iter(cur, acc):
        return acc if cmp_op(cur, stop) else iter(cur + step, acc + [cur])
    return iter(start, [])

def range_step_r(step, start, stop):
    cmp_op = operator.gt if step > 0 else operator.lt
    if cmp_op(start, stop): return []
    else: return [start] + range_step_r(step, start + step, stop)

def range_step_lp(step, start, stop):
    cmp_op = operator.gt if step > 0 else operator.lt
    acc, cur = [], start
    #
    while True:
        if cmp_op(cur, stop): break
        acc += [cur]
        cur = cur + step
    return acc

def range_i(start, stop): return range_step_i(1, start, stop)

def range_r(start, stop): return range_step_r(1, start, stop)

def range_lp(start, stop): return range_step_lp(1, start, stop)


def lib_main(argv=None):
    print('fact(5):', fact_i(5))
    return 0

if '__main__' == __name__:
    sys.exit(lib_main(sys.argv[1:]))
