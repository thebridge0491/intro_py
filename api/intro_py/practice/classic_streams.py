# -*- coding: utf-8 -*-
'''Classic_streams module (lazy sequence (streams) classic examples).

'''

from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import logging, inspect, operator, itertools
#from builtins import (ascii, filter, hex, map, oct, zip)

# __all__ = []


MODULE_LOGGER = logging.getLogger(__name__)

# def _next_row(xss):
##    zip_lst = list(zip([0] + xss, xss + [0]))
##    return list(map(lambda tup: tup[0] + tup[1], zip_lst))
#    return list(map(operator.add, [0] + xss, xss + [0]))


# mut_y -- yield variations (mutating variables version)
# y -- yield variations (non-mutating variables version)
# map2y -- variations using map2_y (yield map 2 lists)
# uy -- yield variations using unfold
# ge -- generator-expression variations

def irange_mut_y(start=0, step=1):     # equivalent itertools.count
    n = start
    while True:
        yield n
        n += step

def squares_mut_y():
    n = 0.0
    while True:
        yield n * n
        n += 1.0

def expts_mut_y(base):
    idx, acc = 0, 1.0
    while True:
        yield acc
        idx += 1 ; acc *= base

def sums_mut_y(lo=0):
    n, acc = lo, lo
    while True:
        yield acc
        n += 1 ; acc = acc + n

def facts_mut_y():
    n, acc = 0, 1
    while True:
        yield acc
        n += 1 ; acc = acc * n

def fibs_mut_y():
    s0, s1 = 0, 1
    while True:
        yield s0
        s1 = s0 + s1 ; s0 = s1 - s0

def pascalrows_mut_y():
    row = [1]
    while True:
        yield row
        row = list(map(operator.add, [0] + row, row + [0]))


def irange_y(start=0, step=1):     # equivalent itertools.count
    yield start
    for i in irange_y(start=(start + step), step=step):
        yield i

def squares_y(lo=0.0):
    yield lo * lo
    for i in squares_y(lo + 1):
        yield i

def expts_y(base, acc=1.0):
    yield acc
    for i in expts_y(base, base * acc):
        yield i

def sums_y(lo=0, acc=0):
    yield acc + lo
    for i in sums_y(lo + 1, acc + lo):
        yield i

def facts_y(n=0, acc=1):
    yield acc
    for i in facts_y(n + 1, acc * (n + 1)):
        yield i

def fibs_y(s0=0, s1=1):
    yield s0
    for i in fibs_y(s1, s0 + s1):
        yield i

def pascalrows_y(acc=None):
    row = acc if acc is not None else [1]
    yield row
    for i in pascalrows_y(list(map(operator.add, [0] + row, row + [0]))):
        yield i



def map2_y(func, xs, ys):
    iterators = list(map(iter, [xs, ys]))
    while True:
        args = [next(it) for it in iterators]
        yield func(*args)

def squares_map2y():
    yield 0.0
    for x in map2_y(lambda a, b: b * b, squares_map2y(), itertools.count(1.0)):
        yield x

def expts_map2y(base):
    yield 1.0
    #for x in map2_y(lambda a, e: base ** e, expts_map2y(base),
    #        itertools.count(1.0)):
    #for x in map2_y(lambda a, e: a * e, expts_map2y(base),
    #        itertools.count(start=base, step=0)):
    for x in map2_y(lambda a, e: a * e, expts_map2y(base),
            itertools.repeat(base)):
        yield x

def sums_map2y(lo=0):
    yield lo
    for x in map2_y(lambda a, e: a + e + lo, sums_map2y(lo),
            itertools.count(1)):
        yield x

def facts_map2y():
    yield 1
    for x in map2_y(lambda a, e: a * e, facts_map2y(), itertools.count(1)):
        yield x

def fibs_map2y():
    yield 0
    yield 1
    res_gen = fibs_map2y() ; next(res_gen)
    for x in map2_y(lambda s0, s1: s0 + s1, fibs_map2y(), res_gen):
        yield x

def pascalrows_map2y():
    yield [1]
    for x in map2_y(lambda row, i: list(map(operator.add, [0] + row,
            row + [0])), pascalrows_map2y(), itertools.count()):
        yield x


def unfold_y(func, seed):
    (a, new_seed) = func(seed)
    yield a
    for cur in unfold_y(func, new_seed):
        yield cur

def squares_uy():
    def ufunc(cnt):
        return (cnt * cnt, cnt + 1)
    return unfold_y(ufunc, 0.0)

def expts_uy(base):
    def ufunc(acc_cnt):
        (acc, cnt) = acc_cnt
        if 0 == cnt: return (1.0, (cnt + 1, 1.0))
        return (acc * base, (acc * base, cnt + 1))
    return unfold_y(ufunc, (1.0, 0))

def sums_uy(lo=0):
    def ufunc(acc_cur):
        (acc, cur) = acc_cur
        return (acc + cur, (acc + cur, cur + 1))
    return unfold_y(ufunc, (0, lo))

def facts_uy():
    def ufunc(acc_cur):
        (acc, cur) = acc_cur
        if 0 == cur: return (1, (1, 1))
        return (acc * cur, (acc * cur, cur + 1))
    return unfold_y(ufunc, (1, 0))

def fibs_uy():
    def ufunc(s0_s1):
        return (s0_s1[0], (s0_s1[1], s0_s1[0] + s0_s1[1]))
    return unfold_y(ufunc, (0, 1))

def pascalrows_uy():
    def ufunc(row):
        return (row, list(map(operator.add, [0] + row, row + [0])))
    return unfold_y(ufunc, [1])


def squares_ge():
    # return (x ** 2.0 for x in itertools.count())
    return (x * x for x in itertools.count(0.0))

def expts_ge(base):
    # return (base ** x for x in itertools.count())
    return (x for x in [1.0] for i in itertools.count()
        for x in [x * base if 0 != i else 1.0])

def sums_ge(lo=0):
    return (x for x in [0] for i in itertools.count(lo) for x in [x + i])

def facts_ge():
    return (x for x in [1] for i in itertools.count()
        for x in [x * i if 0 != i else 1])

def fibs_ge():
    return (s0 for [s0, s1] in [[0, 1]] for i in itertools.count()
        for [s0, s1] in [[s1, s0 + s1] if 0 != i else [0, 1]])

def pascalrows_ge():
    return (row for row in [[1]] for i in itertools.count()
        for row in [list(map(operator.add, [0] + row, row + [0]))
        if 0 != i else [1]])


def lib_main(argv=None):
    res_gen = facts_y()
    print('res_gen = facts_y() ; [next(res_gen) for i in range(5 + 1)]',
        [next(res_gen) for i in range(5 + 1)])
    return 0

if '__main__' == __name__:
    sys.exit(lib_main(sys.argv[1:]))
