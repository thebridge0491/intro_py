# -*- coding: utf-8 -*-
'''Sequenceops_variadic module (variadic sequence ops functions).

'''

from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import logging, inspect, operator
from functools import reduce
#from builtins import (ascii, filter, hex, map, oct, zip)

# __all__ = []


MODULE_LOGGER = logging.getLogger(__name__)

# _lpv -- loop variations
# _yv -- yield variations
# _fv -- fold variations 
# _lcv -- list-comprehension variations

def anyall_lpv(pred, *lsts):
    func = lambda acc, lst: (acc[0] or any(map(pred, lst)), 
        acc[1] and all(map(pred, lst)))
    acc = (False, True)
    for lst in lsts: acc = func(acc, lst)
    return acc

def any_lpv(pred, *lsts): return anyall_lpv(pred, *lsts)[0]

def all_lpv(pred, *lsts): return anyall_lpv(pred, *lsts)[1]

def map_lpv(func, *lsts):
    acc, iterators = [], list(map(iter, lsts))
    while True:
        try:
            args = [next(it) for it in iterators]
            acc = acc + [func(*args)]
        except StopIteration as exc:
            break
    return acc

def foreach_lpv(func, *lsts):
    acc, iterators = [], list(map(iter, lsts))
    while True:
        try:
            args = [next(it) for it in iterators]
            acc = acc + [func(*args)]
        except StopIteration as exc:
            break
    return acc

def fold_left_lpv(corp, init, *lsts):
    acc, iterators = init, list(map(iter, lsts))
    while True:
        try:
            args = [next(it) for it in iterators]
            acc = corp(acc, *args)
        except StopIteration as exc:
            break
    return acc

def fold_right_lpv(proc, init, *lsts):
    acc, iterators = init, list(map(iter, map(reversed, lsts)))
    while True:
        try:
            args = [next(it) for it in iterators]
            acc = proc(acc, *args)
        except StopIteration as exc:
            break
    return acc

def append_lpv(*lsts):
    acc = []
    for lst in lsts: acc += lst
    return acc

def zip_lpv(*lsts): return map_lpv(lambda *args: tuple(args), *lsts)


def anyall_yv(init, pred, *lsts):
    func = lambda acc, lst: (acc[0] or any(map(pred, lst)), 
        acc[1] and all(map(pred, lst)))
    acc = (False, True)
    try:
        for lst in lsts:
            acc = func(acc, lst)
            yield acc[0] if False == init else acc[1]
    except StopIteration as exc:
        return

def any_yv(pred, *lsts): return anyall_yv(False, pred, *lsts)

def all_yv(pred, *lsts): return anyall_yv(True, pred, *lsts)

def map_yv(func, *lsts):
    iterators = list(map(iter, lsts))
    try:
        while True:
            args = [next(it) for it in iterators]
            yield func(*args)
    except StopIteration as exc:
        return

def foreach_yv(func, *lsts):
    iterators = list(map(iter, lsts))
    try:
        while True:
            args = [next(it) for it in iterators]
            yield func(*args)
    except StopIteration as exc:
        return

def fold_left_yv(corp, init, *lsts):
    acc, iterators = init, list(map(iter, lsts))
    try:
        while True:
            args = [next(it) for it in iterators]
            acc = corp(acc, *args)
            yield acc
    except StopIteration as exc:
        return

def fold_right_yv(proc, init, *lsts):
    acc, iterators = init, list(map(iter, map(reversed, lsts)))
    try:
        while True:
            args = [next(it) for it in iterators]
            acc = proc(acc, *args)
            yield acc
    except StopIteration as exc:
        return

def append_yv(*lsts):
    acc = []
    try:
        for lst in lsts:
            acc += lst
            yield acc
    except StopIteration as exc:
        return

def zip_yv(*lsts): return map_yv(lambda *args: tuple(args), *lsts)


def anyall_fv(pred, *lsts):
    func = lambda acc, lst: (acc[0] or any(map(pred, lst)), 
        acc[1] and all(map(pred, lst)))
    acc = (False, True)
    return reduce(lambda a, args: func(a, args), lsts, acc)

def any_fv(pred, *lsts): return anyall_fv(pred, *lsts)[0]

def all_fv(pred, *lsts): return anyall_fv(pred, *lsts)[1]

def map_fv(func, *lsts):
    return reduce(lambda a, args: a + [func(*args)], zip(*lsts), [])

def foreach_fv(func, *lsts):
    return reduce(lambda a, args: a + [func(*args)], zip(*lsts), [])

def append_fv(*lsts): return reduce(lambda a, el: a + el, lsts, [])

def zip_fv(*lsts): return map_fv(lambda *args: tuple(args), *lsts)


def anyall_lcv(pred, *lsts):
    func = lambda acc, lst: (acc[0] or any(map(pred, lst)), 
        acc[1] and all(map(pred, lst)))
    acc = (False, True)
    return ([(False, True)] + [a for a in [(False, True)] for el in lsts
        for a in [func(a, el)]])[-1]

def any_lcv(pred, *lsts): return anyall_lcv(pred, *lsts)[0]

def all_lcv(pred, *lsts): return anyall_lcv(pred, *lsts)[1]

def map_lcv(func, *lsts): return [func(*el) for el in zip(*lsts)]

def foreach_lcv(func, *lsts): return [func(*el) for el in zip(*lsts)]

def append_lcv(*lsts):
    return [acc for acc in [[]] for el in lsts for acc in [acc + el]][-1]

def zip_lcv(*lsts): return map_lcv(lambda *args: tuple(args), *lsts)


def lib_main(argv=None):
    print('map_fv(lambda e1, e2: e1 + e2, *[[5, 15], [3, 13]]):',
        map_fv(lambda e1, e2: e1 + e2, *[[5, 15], [3, 13]]))
    return 0

if '__main__' == __name__:
    sys.exit(lib_main(sys.argv[1:]))
