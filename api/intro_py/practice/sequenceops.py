# -*- coding: utf-8 -*-
'''Sequence operations module

'''

from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import sys, logging, inspect, operator
from future.builtins import (ascii, filter, hex, map, oct, zip, range)

from .sequenceops_hiorder import (tabulate_f, length_f, nth_f, index_f,
    find_f, min_f, max_f, reverse_f, copy_of_f, take_f, drop_f, split_at_f,
    any_f, all_f, map_f, foreach_f, filter_f, remove_f, partition_f,
    is_ordered_f,
    
    append_f, interleave_f, map2_f, zip_f, unzip_f, concat_f, flatten_f,
    
    
    tabulate_u, length_u, nth_u, index_u, find_u, min_u, max_u, reverse_u, copy_of_u, split_at_u, take_u, drop_u, any_u, all_u, map_u,
    foreach_u, partition_u, filter_u, remove_u, is_ordered_u,
    
    append_u, interleave_u, map2_u, zip_u, unzip_u, concat_u,
    
    
    tabulate_lc, length_lc, nth_lc, index_lc, find_lc, min_lc, max_lc,
    reverse_lc, copy_of_lc, take_lc, drop_lc, split_at_lc, any_lc, all_lc,
    map_lc, foreach_lc, filter_lc, remove_lc, partition_lc, is_ordered_lc,
    
    append_lc, interleave_lc, map2_lc, zip_lc, unzip_lc, concat_lc,
    
    
    tabulate_imap, nth_islice, take_islice, drop_islice, split_at_islice,
    concat_chain
)
from .sequenceops_variadic import (any_lpv, all_lpv, map_lpv, foreach_lpv,
    fold_left_lpv, fold_right_lpv, append_lpv, zip_lpv, 
    
    any_yv, all_yv, map_yv, foreach_yv, fold_left_yv, fold_right_yv,
    append_yv, zip_yv,
    
    any_fv, all_fv, map_fv, foreach_fv, append_fv, zip_fv,
    
    any_lcv, all_lcv, map_lcv, foreach_lcv, append_lcv, zip_lcv
)

__all__ = ['tabulate_i', 'tabulate_r', 'tabulate_lp', 'length_i', 'length_r',
    'length_lp', 'nth_i', 'nth_r', 'nth_lp', 'index_i', 'index_r', 'index_lp',
    'find_i', 'find_r', 'find_lp', 'min_i', 'min_r', 'min_lp', 'max_i',
    'max_r', 'max_lp', 'reverse_i', 'reverse_r', 'reverse_lp',
    'reverse_mut_i', 'reverse_mut_lp', 'copy_of_i', 'copy_of_r', 'copy_of_lp',
    'take_i', 'take_lp', 'drop_i', 'drop_lp', 'split_at_i', 'split_at_lp',
    'any_i', 'any_r', 'any_lp', 'all_i', 'all_r', 'all_lp', 'map_i', 'map_r',
    'map_lp', 'foreach_i', 'foreach_r', 'foreach_lp', 'filter_i', 'filter_r',
    'filter_lp', 'remove_i', 'remove_r', 'remove_lp', 'partition_i',
    'partition_r', 'partition_lp', 'fold_left_i', 'fold_left_r',
    'fold_left_lp', 'fold_right_i', 'fold_right_r', 'fold_right_lp',
    'unfold_right_i', 'unfold_right_lp', 'unfold_left_r', 'unfold_left_lp',
    'is_ordered_i', 'is_ordered_r', 'is_ordered_lp', 'quick_sort',

    'append_i', 'append_r', 'append_lp', 'interleave_i', 'interleave_r',
    'interleave_lp', 'map2_i', 'map2_r', 'map2_lp', 'zip_i', 'zip_r',
    'zip_lp', 'unzip_i', 'concat_i', 'concat_r', 'concat_lp', 'flatten_r',
    
    
    'tabulate_f', 'length_f', 'nth_f', 'index_f', 'find_f', 'min_f', 'max_f',
    'reverse_f', 'copy_of_f', 'take_f', 'drop_f', 'split_at_f', 'any_f',
    'all_f', 'map_f', 'foreach_f', 'filter_f', 'remove_f', 'partition_f',
    'is_ordered_f',
    
    'append_f', 'interleave_f', 'map2_f', 'zip_f', 'unzip_f', 'concat_f',
    'flatten_f',
    
    
    'tabulate_u', 'length_u', 'nth_u', 'index_u', 'find_u', 'min_u', 'max_u',
    'reverse_u', 'copy_of_u', 'split_at_u', 'take_u',
    'drop_u', 'any_u', 'all_u', 'map_u', 'foreach_u', 'partition_u',
    'filter_u', 'remove_u', 'is_ordered_u',
    
    'append_u', 'interleave_u', 'map2_u', 'zip_u', 'unzip_u', 'concat_u',
    
    
    'tabulate_lc', 'length_lc', 'nth_lc', 'index_lc', 'find_lc', 'min_lc',
    'max_lc', 'reverse_lc', 'copy_of_lc', 'take_lc', 'drop_lc', 'split_at_lc',
    'any_lc', 'all_lc', 'map_lc', 'foreach_lc', 'filter_lc', 'remove_lc',
    'partition_lc', 'is_ordered_lc',
    'append_lc', 'interleave_lc', 'map2_lc', 'zip_lc', 'unzip_lc',
    'concat_lc',
    
    
    'tabulate_imap', 'nth_islice', 'take_islice', 'drop_islice',
    'split_at_islice', 'concat_chain',
    
    
    'any_lpv', 'all_lpv', 'map_yv', 'foreach_yv', 'fold_left_lpv',
    'fold_right_lpv', 'append_lpv', 'zip_yv',
    'map_lpv', 'foreach_lpv', 'fold_left_yv', 'fold_right_yv', 'zip_lpv',
    'any_yv', 'all_yv', 'append_yv', 'any_fv', 'all_fv', 'map_fv',
    'foreach_fv', 'zip_fv', 'append_fv', 'append_lcv', 'map_lcv',
    'foreach_lcv', 'zip_fv', 'any_lcv', 'all_lcv'
    ]


MODULE_LOGGER = logging.getLogger(__name__)

def swap(idx0, idx1, lst):
    lst[idx0], lst[idx1] = lst[idx1], lst[idx0]

def tabulate_i(func, cnt):
    def iter(idx, acc):
        return acc if cnt <= idx else iter(idx + 1, acc + [func(idx)])
    return iter(0, [])

def tabulate_r(func, cnt):
    return [] if 0 >= cnt else tabulate_r(func, cnt - 1) + [func(cnt - 1)]

def tabulate_lp(func, cnt):
    acc, idx = [], 0
    while cnt > idx:
        acc += [func(idx)]
        idx += 1
    return acc

def length_i(lst):
    def iter(acc, rst):
        return acc if [] == rst else iter(acc + 1, rst[1:])
    return iter(0, lst)

def length_r(lst):
    return 0 if [] == lst else 1 + length_r(lst[1:])

def length_lp(lst):
    acc = 0
    for el in lst: acc += 1
    return acc

def nth_i(idx, lst):
    def iter(ndx, rst):
        if [] == rst: return None
        elif 0 >= ndx: return rst[0]
        else: return iter(ndx - 1, rst[1:])
    return iter(idx, lst)

def nth_r(idx, lst):
    if [] == lst: return None
    elif 0 >= idx: return lst[0]
    else: return nth_r(idx - 1, lst[1:])

def nth_lp(idx, lst):
    for i in range(len(lst)):
        if idx <= i: return lst[i]
    return None

def index_find_i(data, lst, idx=0):
    def iter(rst, idx):
        if [] == rst: return (-1, None)
        elif data == rst[0]: return (idx, rst[0])
        else: return iter(rst[1:], idx + 1)
    return iter(lst, 0)

def index_i(data, lst): return index_find_i(data, lst)[0]

def find_i(data, lst): return index_find_i(data, lst)[1]

def index_find_r(data, lst, idx=0):
    if [] == lst: return (-1, None)
    elif data == lst[0]: return (idx, lst[0])
    else: return index_find_r(data, lst[1:], idx=idx+1)

def index_r(data, lst): return index_find_r(data, lst)[0]

def find_r(data, lst): return index_find_r(data, lst)[1]

def index_find_lp(data, lst, idx=0):
    for i in range(0, len(lst)):
        if data == lst[i]: return (i, lst[i])
    return (-1, None)

def index_lp(data, lst): return index_find_lp(data, lst)[0]

def find_lp(data, lst): return index_find_lp(data, lst)[1]

def minmax_i(lst):
    if [] == lst: raise Exception('empty list')
    def iter(lo, hi, rst):
        if [] == rst: return (lo, hi)
        else:
            if rst[0] < lo: return iter(rst[0], hi, rst[1:])
            elif rst[0] > hi: return iter(lo, rst[0], rst[1:])
            else: return iter(lo, hi, rst[1:])
    return iter(lst[0], lst[0], lst[1:])

def min_i(lst): return minmax_i(lst)[0]

def max_i(lst): return minmax_i(lst)[1]

def minmax_r(lst):
    def helper_r(norm, rst):
        if [] == rst: raise Exception('empty list')
        elif 1 == len(rst): return rst[0]
        else:
            if norm(rst[0] < rst[1]):
                return helper_r(norm, [rst[0]] + rst[2:])
            else: return helper_r(norm, rst[1:])
    return (helper_r(operator.truth, lst), helper_r(operator.not_, lst))

def min_r(lst): return minmax_r(lst)[0]

def max_r(lst): return minmax_r(lst)[1]

def minmax_lp(lst):
    if [] == lst: raise Exception('empty list')
    lo, hi = lst[0], lst[0]
    for el in lst[1:]:
        if el < lo: lo = el
        elif el > hi: hi = el
    return (lo, hi)

def min_lp(lst): return minmax_lp(lst)[0]

def max_lp(lst): return minmax_lp(lst)[1]

def reverse_i(lst):
    func_name = inspect.stack()[0][3]
    MODULE_LOGGER.info(func_name + '()')
    #
    def iter(idx, acc):
        return acc if 0 > idx else iter(idx - 1, acc + [lst[idx]])
    return iter(len(lst) - 1, [])

def reverse_r(lst):
    return [] if [] == lst else [lst[-1]] + reverse_r(lst[:-1])

def reverse_lp(lst):
    newlst = []
    for i in range(len(lst) - 1, -1, -1): newlst.append(lst[i])
    return newlst

def reverse_mut_i(lst):
    def iter(i, j):
        if i >= j: return
        else:
            swap(i, j, lst)
            return iter(i + 1, j - 1)
    iter(0, len(lst) - 1)

def reverse_mut_lp(lst):
    for i in range(0, len(lst) // 2):
        swap(i, len(lst) - 1 - i, lst)

def copy_of_i(lst):
    def iter(idx, acc):
        return acc if 0 > idx else iter(idx - 1, [lst[idx]] + acc)
    return iter(len(lst) - 1, [])

def copy_of_r(lst):
    # return lst[:]
    return [] if 0 == len(lst) else copy_of_r(lst[:-1]) + [lst[-1]]

def copy_of_lp(lst):
    newlst = []
    for i in range(len(lst)):
        newlst.append(lst[i])
    return newlst

def split_at_i(num, lst):
    def iter(cur, acc, rst):
        if [] == rst or 0 == cur: return (acc, rst)
        else: return iter(cur - 1, acc + [rst[0]], rst[1:])
    return iter(num, [], lst)

def take_i(num, lst): return split_at_i(num, lst)[0]

def drop_i(num, lst): return split_at_i(num, lst)[1]

def split_at_lp(num, lst):
    cur, acc, rst = num, [], lst
    while [] != rst and 0 != cur:
        acc += [rst[0]]
        cur -= 1
        rst = rst[1:]
    return (acc, rst)

def take_lp(num, lst): return split_at_lp(num, lst)[0]

def drop_lp(num, lst): return split_at_lp(num, lst)[1]

def anyall_i(pred, lst):
    def iter(acc, rst):
        if [] == rst: return acc
        return iter((acc[0] or pred(rst[0]), acc[1] and pred(rst[0])), rst[1:])
    return iter((False, True), lst)

def any_i(pred, lst): return anyall_i(pred, lst)[0]

def all_i(pred, lst): return anyall_i(pred, lst)[1]

def anyall_r(pred, lst):
    if [] == lst: return (False, True)
    return (pred(lst[0]) or anyall_r(pred, lst[1:])[0], 
        pred(lst[0]) and anyall_r(pred, lst[1:])[1])

def any_r(pred, lst): return anyall_r(pred, lst)[0]

def all_r(pred, lst): return anyall_r(pred, lst)[1]

def anyall_lp(pred, lst):
    acc = (False, True)
    for el in lst:
        acc = (acc[0] or pred(el), acc[1] and pred(el))
    return acc

def any_lp(pred, lst): return anyall_lp( pred, lst)[0]

def all_lp(pred, lst): return anyall_lp(pred, lst)[1]

def map_i(func, lst):
    def iter(rst, acc):
        return acc if [] == rst else iter(rst[1:], acc + [func(rst[0])])
    return iter(lst, [])

def map_r(func, lst):
    return [] if [] == lst else [func(lst[0])] + map_r(func, lst[1:])

def map_lp(func, lst):
    acc = []
    for el in lst: acc += [func(el)]
    return acc

def foreach_i(func, lst):
    def iter(rst):
        if [] == rst: return
        func(rst[0])
        return iter(rst[1:])
    return iter(lst)

def foreach_r(func, lst):
    if [] == lst: return
    func(lst[0])
    return foreach_r(func, lst[1:])

def foreach_lp(func, lst):
    for el in lst:
        func(el)

def partition_i(pred, lst):
    def iter(rst, acc):
        if [] == rst: return acc
        elif pred(rst[0]): return iter(rst[1:], (acc[0] + [rst[0]], acc[1]))
        else: return iter(rst[1:], (acc[0], acc[1] + [rst[0]]))
    return iter(lst, ([], []))

def filter_i(pred, lst): return partition_i(pred, lst)[0]

def remove_i(pred, lst): return partition_i(pred, lst)[1]

def partition_r(pred, lst):
    def helper_r(norm, rst):
        if [] == rst: return []
        elif norm(pred(rst[0])): return [rst[0]] + helper_r(norm, rst[1:])
        else: return helper_r(norm, rst[1:])
    return (helper_r(operator.truth, lst), helper_r(operator.not_, lst))

def filter_r(pred, lst): return partition_r(pred, lst)[0]

def remove_r(pred, lst): return partition_r(pred, lst)[1]

def partition_lp(pred, lst):
    acc_f, acc_r = [], []
    for el in lst:
        if pred(el): acc_f += [el]
        else: acc_r += [el]
    return (acc_f, acc_r)

def filter_lp(pred, lst): return partition_lp(pred, lst)[0]

def remove_lp(pred, lst): return partition_lp(pred, lst)[1]

def fold_left_i(corp, init, lst):
    def iter(acc, rst):
        return acc if [] == rst else iter(corp(acc, rst[0]), rst[1:])
    return iter(init, lst)

def fold_left_r(corp, init, lst):
    return init if [] == lst else fold_left_r(corp, corp(init, lst[0]), lst[1:])

def fold_left_lp(corp, init, lst):
    acc = init
    for el in lst: acc = corp(acc, el)
    return acc

def fold_right_i(proc, lst, init):
    def iter(rst, acc):
        return acc if [] == rst else iter(rst[:-1], proc(rst[-1], acc))
    return iter(lst, init)

def fold_right_r(proc, lst, init):
    if [] == lst: return init
    # return fold_right_r(proc, lst[:-1], proc(init, lst[-1]))
    return proc(lst[0], fold_right_r(proc, lst[1:], init))

def fold_right_lp(proc, lst, init):
    acc = init
    for el in reversed(lst): acc = proc(el, acc)
    return acc

def unfold_right_i(func, seed):
    def iter(cur, acc):
        if func(cur) is None: return acc
        (a, new_seed) = func(cur)
        return iter(new_seed, [a] + acc)
    return iter(seed, [])

def unfold_right_lp(func, seed):
    acc, cur = [], seed
    while func(cur) is not None:
        (a, new_seed) = func(cur)
        acc = [a] + acc
        cur = new_seed
    return acc

def unfold_left_r(func, seed):
    if func(seed) is None: return []
    (a, new_seed) = func(seed)
    return [a] + unfold_left_r(func, new_seed)

def unfold_left_lp(func, seed):
    acc, cur = [], seed
    while func(cur) is not None:
        (a, new_seed) = func(cur)
        acc = acc + [a]
        cur = new_seed
    return acc

#def cmp(x, y):
#    return ((x > y) - (x < y))

def _flip_func(func, is_flipped=True):
    return (lambda *args: func(*reversed(args))) if is_flipped else func

def _norm_le(x, y, reverse=False): return x >= y if reverse else x <= y
def _norm_gt(x, y, reverse=False): return x < y if reverse else x > y

#def is_ordered_i(lst, cmp_func=cmp):
#    def iter(rst, acc):
#        if 1 >= len(rst): return acc
#        return iter(rst[1:], acc and 1 > cmp_func(rst[0], rst[1]))
#    return iter(lst, True)
#
#def is_ordered_r(lst, cmp_func=cmp):
#    if 1 >= len(lst): return True
#    return 1 > cmp_func(lst[0], lst[1]) and is_ordered_r(lst[1:], cmp_func)
#
#def is_ordered_lp(lst, cmp_func=cmp):
#    if 1 >= len(lst): return True
#    acc, oldval = True, lst[0]
#    for el in lst[1:]:
#        acc = acc and 1 > cmp_func(oldval, el)
#        oldval = el
#    return acc

def is_ordered_i(lst, key_func=None, reverse=False):
    if None == key_func: key_func = lambda x: x
    _flip_le = _flip_func(operator.le, reverse)
    def iter(rst, acc):
        if 2 > len(rst): return acc
        return iter(rst[1:], acc and
            _flip_le(key_func(rst[0]), key_func(rst[1])))
    return iter(lst, True)

def is_ordered_r(lst, key_func=None, reverse=False):
    if None == key_func: key_func = lambda x: x
    _flip_le = _flip_func(operator.le, reverse)
    if 2 > len(lst): return True
    return _flip_le(key_func(lst[0]), key_func(lst[1])) and \
        is_ordered_r(lst[1:], key_func, reverse)

def is_ordered_lp(lst, key_func=None, reverse=False):
    if None == key_func: key_func = lambda x: x
    acc, oldval, _flip_le = True, lst[0], _flip_func(operator.le, reverse)
    if 2 > len(lst): return True
    for el in lst[1:]:
        acc = acc and _flip_le(key_func(oldval), key_func(el))
        oldval = el
    return acc

#def _partition_helper(lst, lo, hi, cmp_func=cmp):
#    lwr, upr = lo, hi
#    while lwr < upr:
#        while 1 > cmp_func(lst[lwr], lst[lo]) and lwr < upr: lwr += 1
#        while 0 < cmp_func(lst[upr], lst[lo]): upr -= 1
#        if lwr < upr: swap(lwr, upr, lst)
#    swap(lo, upr, lst)
#    return upr
#
#def quick_sort(lst, lo, hi, cmp_func=cmp):
#    import random
#    if hi > lo:
#        rnd_ndx = random.randrange(hi - lo + 1) + lo
#        swap(lo, rnd_ndx, lst)
#        split = _partition_helper(lst, lo, hi, cmp_func)
#        quick_sort(lst, lo, split - 1, cmp_func)
#        quick_sort(lst, split + 1, hi, cmp_func)

def _partition_helper(lst, lo, hi, key_func=None, reverse=False):
    if None == key_func: key_func = lambda x: x
    _flip_le = _flip_func(operator.le, reverse)
    _flip_gt = _flip_func(operator.gt, reverse)
    lwr, upr = lo, hi
    while lwr < upr:
        while _flip_le(key_func(lst[lwr]), key_func(lst[lo])) and lwr < upr:
            lwr += 1
        while _flip_gt(key_func(lst[upr]), key_func(lst[lo])): upr -= 1
        if lwr < upr: swap(lwr, upr, lst)
    swap(lo, upr, lst)
    return upr

def quick_sort(lst, lo, hi, key_func=None, reverse=False):
    import random
    if hi > lo:
        rnd_ndx = random.randrange(lo, hi + 1)
        swap(lo, rnd_ndx, lst)
        split = _partition_helper(lst, lo, hi, key_func, reverse)
        quick_sort(lst, lo, split - 1, key_func, reverse)
        quick_sort(lst, split + 1, hi, key_func, reverse)


def append_i(xss, yss):
    def iter(rst, acc):
        return acc if [] == rst else iter(rst[1:], acc + [rst[0]])
    return iter(yss, xss)

def append_r(xss, yss):
    return yss if [] == xss else [xss[0]] + append_r(xss[1:], yss)

def append_lp(xss, yss):
    acc = xss[:]
    for el in yss: acc += [el]
    return acc

def interleave_i(xss, yss):
    len_short = len(xss) if len(xss) < len(yss) else len(yss)
    init = xss[len_short:] + yss[len_short:]
    def iter(wss, zss, acc):
        if [] == wss: return acc + init
        return iter(wss[1:], zss[1:], acc + [wss[0], zss[0]])
    return iter(xss[:len_short], yss[:len_short], [])

def interleave_r(xss, yss):
    return yss if [] == xss else [xss[0]] + interleave_r(yss, xss[1:])

def interleave_lp(xss, yss):
    len_short = len(xss) if len(xss) < len(yss) else len(yss)
    acc, init = [], xss[len_short:] + yss[len_short:]
    for i in range(len_short):
        acc += [xss[i], yss[i]]
    return acc + init

def map2_i(func, xss, yss):
    def iter(wss, zss, acc):
        if [] == wss or [] == zss: return acc
        return iter(wss[1:], zss[1:], acc + [func(wss[0], zss[0])])
    return iter(xss, yss, [])

def map2_r(func, xss, yss):
    if [] == xss or [] == yss: return []
    return [func(xss[0], yss[0])] + map2_r(func, xss[1:], yss[1:])

def map2_lp(func, xss, yss):
    acc, wss, zss = [], xss, yss
    while [] != wss and [] != zss:
        acc += [func(wss[0], zss[0])]
        wss = wss[1:]
        zss = zss[1:]
    return acc

def zip_i(xss, yss): return map2_i(lambda *args: tuple(args), xss, yss)

def zip_r(xss, yss): return map2_r(lambda *args: tuple(args), xss, yss)

def zip_lp(xss, yss): return map2_lp(lambda *args: tuple(args), xss, yss)

def unzip_i(ziplst):
    def iter(rst, xss_yss):
        (xss, yss) = xss_yss
        if [] == rst: return [tuple(xss), tuple(yss)]
        return iter(rst[1:], (xss + [rst[0][0]], yss + [rst[0][1]]))
    return iter(ziplst, ([], []))

def concat_i(nlsts):
    def iter(rst, acc):
        return acc if [] == rst else iter(rst[1:], acc + rst[0])
    return iter(nlsts, [])

def concat_r(nlsts):
    return [] if [] == nlsts else nlsts[0] + concat_r(nlsts[1:])

def concat_lp(nlsts):
    acc = []
    for lst in nlsts:
        acc = acc + lst
    return acc

def flatten_r(nlsts):
    if [] == nlsts: return []
    elif not isinstance(nlsts, list): return [nlsts]
    return flatten_r(nlsts[0]) + flatten_r(nlsts[1:])


def lib_main(argv=None):
    print('index(3, [4, 2, 0, 1, 3]):', index_i(3, [4, 2, 0, 1, 3]))
    return 0

if '__main__' == __name__:
    sys.exit(lib_main(sys.argv[1:]))
