# -*- coding: utf-8 -*-
'''Sequence ops hiorder module (variations using higher-order functions).

'''

from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import logging, inspect, operator, itertools
from functools import reduce
#from builtins import (ascii, filter, hex, map, oct, zip, range)

from intro_py import util


MODULE_LOGGER = logging.getLogger(__name__)

def _flip_func(func, is_flipped=True):
    return (lambda *args: func(*reversed(args))) if is_flipped else func

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


def tabulate_f(func, cnt):
    return reduce(lambda a, i: a + [func(i)], range(cnt), [])

def length_f(lst): return reduce(lambda a, e: a + 1, lst, 0)

def nth_f(idx, lst):
    return reduce(lambda acc, i_e: i_e[1] if idx == i_e[0] else acc,
        enumerate(lst), None)

def index_find_f(data, lst, idx=0):
    return reduce(lambda idx_fnd, i_e: (i_e[0], i_e[1])if -1 == idx_fnd[0]
        and data == i_e[1] else idx_fnd, enumerate(lst), (-1, None))

def index_f(data, lst): return index_find_f(data, lst)[0]

def find_f(data, lst): return index_find_f(data, lst)[1]

def minmax_f(lst):
    if [] == lst: raise Exception('empty list')
    return reduce(lambda lo_hi, e: (e, lo_hi[1]) if lo_hi[0] > e
        else (lo_hi[0], e) if lo_hi[1] < e else lo_hi, lst[1:],
        (lst[0], lst[0]))

def min_f(lst): return minmax_f(lst)[0]

def max_f(lst): return minmax_f(lst)[1]

def reverse_f(lst): return reduce(lambda a, e: [e] + a, lst, [])

    # return lst[:]
def copy_of_f(lst): return reduce(lambda a, e: a + [e], lst, [])

def split_at_f(num, lst):
    return reduce(lambda at_ad, i_e: (at_ad[0] + [i_e[1]], at_ad[1])
        if num > i_e[0] else (at_ad[0], at_ad[1] + [i_e[1]]),
        enumerate(lst), ([], []))

#        return reduce(lambda a, i_e: a + [i_e[1]] if num > i_e[0] else a,
#            enumerate(lst), [])
def take_f(num, lst): return split_at_f(num, lst)[0]

#        return reduce(lambda a, i_e: a + [i_e[1]] if num <= i_e[0] else a,
#            enumerate(lst), [])
def drop_f(num, lst): return split_at_f(num, lst)[1]

def anyall_f(pred, lst):
    func = lambda acc, e: (acc[0] or pred(e), acc[1] and pred(e))
    return reduce(func, lst, (False, True))

def any_f(pred, lst): return anyall_f(pred, lst)[0]

def all_f(pred, lst): return anyall_f(pred, lst)[1]

def map_f(func, lst): return reduce(lambda a, e: a + [func(e)], lst, [])

def foreach_f(func, lst): return reduce(lambda a, e: func(e), lst, None)

def partition_f(pred, lst):
    return reduce(lambda af_ar, e: (af_ar[0] + [e], af_ar[1]) if pred(e)
        else (af_ar[0], af_ar[1] + [e]), lst, ([], []))

#       return reduce(lambda a, e: a + [e] if pred(e) else a, lst, [])
def filter_f(pred, lst): return partition_f(pred, lst)[0]

#       return reduce(lambda a, e: a + [e] if not pred(e) else a, lst, [])
def remove_f(pred, lst): return partition_f(pred, lst)[1]


def is_ordered_f(xss, key_func=None, reverse=False):
    if None == key_func: key_func = lambda x: x
    _flip_le = _flip_func(operator.le, reverse)
    if 2 > len(xss): return True
    return (reduce(lambda old_acc, e: (e, old_acc[1] and
        _flip_le(old_acc[0], e)), xss[1:], (xss[0], True)))[1]


def append_f(xss, yss): return reduce(lambda a, e: a + [e], yss, xss[:])

def interleave_f(xss, yss):
    len_short = len(xss) if len(xss) < len(yss) else len(yss)
    init = xss[len_short:] + yss[len_short:]
    return (reduce(lambda wss_acc, y: (wss_acc[0][:-1],
        [wss_acc[0][-1], y] + wss_acc[1]),
        reversed(yss[:len_short]), (xss[:len_short], init)))[1]

def map2_f(func, xss, yss):
    #return reduce(lambda a, (e1, e2): a + [func(e1, e2)], zip(xss, yss), [])
    len_short = len(xss) if len(xss) < len(yss) else len(yss)
    return reduce(lambda a, i: a + [func(xss[i], yss[i])],
        range(len_short), [])

def zip_f(xss, yss): return map2_f(lambda *args: tuple(args), xss, yss)

def unzip_f(ziplst):
    return reduce(lambda ah_at, eh_et: [ah_at[0] + (eh_et[0],),
        ah_at[1] + (eh_et[1],)], ziplst, [(), ()])

def concat_f(nlsts):
    return reduce(lambda a, e: e + a, reversed(nlsts), [])

def flatten_f(nlsts):
    return reduce(lambda a, e: a + flatten_f(e) if isinstance(e, list)
        else a + [e], nlsts, [])


def tabulate_u(func, cnt):
    def ufunc(idx):
        return None if cnt <= idx else (func(idx), idx + 1)
    #return list(reversed(unfold_right_i(ufunc, 0)))
    return unfold_left_r(ufunc, 0)

def length_u(lst):
    def ufunc(cnt_rst):
        if [] == cnt_rst[1]: return None
        return (cnt_rst[0] + 1, (cnt_rst[0] + 1, cnt_rst[1][1:]))
    return util.head_or(0, unfold_right_i(ufunc, (0, lst)))

def nth_u(idx, lst):
    def gen_func(el, acc, ndx):
        return el if idx == ndx else acc
    def ufunc(acc_ndx_rst):
        (acc, ndx, rst) = acc_ndx_rst
        if [] == rst: return None
        return (gen_func(rst[0], acc, ndx), (gen_func(rst[0], acc, ndx),
            ndx + 1, rst[1:]))
    return util.head_or(None, unfold_right_i(ufunc, (None, 0, lst)))

def index_find_u(data, lst, idx=0):
    def gen_func(el, idx_fnd, ndx):
        return (ndx, el) if -1 == idx_fnd[0] and data == el else idx_fnd
    def ufunc(acc_ndx_rst):
        (acc, ndx, rst) = acc_ndx_rst
        if [] == rst: return None
        return (gen_func(rst[0], acc, ndx), (gen_func(rst[0], acc, ndx),
            ndx + 1, rst[1:]))
    return util.head_or(-1, unfold_right_i(ufunc, ((-1, None), 0, lst)))

def index_u(data, lst): return index_find_u(data, lst)[0]

def find_u(data, lst): return index_find_u(data, lst)[1]

def minmax_u(lst):
    if [] == lst: raise Exception('empty list')
    def gen_func(el, lo_hi):
        (lo, hi) = lo_hi
        return (el, hi) if lo > el else (lo, el) if hi < el else (lo, hi)
    def ufunc(lo_hi_rst):
        ((lo, hi), rst) = lo_hi_rst
        if [] == rst: return None
        return (gen_func(rst[0], (lo, hi)), (gen_func(rst[0], (lo, hi)),
            rst[1:]))
    return util.head_or((lst[0], lst[0]), unfold_right_i(ufunc,
        ((lst[0], lst[0]), lst[1:])))

def min_u(lst): return minmax_u(lst)[0]

def max_u(lst): return minmax_u(lst)[1]

def reverse_u(lst):
    def ufunc(rst):
        return None if [] == rst else (rst[0], rst[1:])
    return unfold_right_i(ufunc, lst)

def copy_of_u(lst):
    def ufunc(rst):
        return None if [] == rst else (rst[0], rst[1:])
    #return list(reversed(unfold_right_i(ufunc, lst)))
    return unfold_left_r(ufunc, lst)

def split_at_u(num, lst):
    def ufunc(wss_zss_ndx):
        ((wss, zss), ndx) = wss_zss_ndx
        if [] == zss or num <= ndx: return None
        return ((wss + [zss[0]], zss[1:]), ((wss + [zss[0]], zss[1:]),
            ndx + 1))
    return util.head_or(([], lst), unfold_right_i(ufunc, (([], lst), 0)))

#               def ufunc(acc_ndx):
#                   (acc, ndx) = acc_ndx
#                   if [] == lst[ndx:] or num <= ndx: return None
#                   return (acc + [lst[ndx]], (acc + [lst[ndx]], ndx + 1))
#               return util.head_or([], unfold_right_i(ufunc, ([], 0)))
def take_u(num, lst): return split_at_u(num, lst)[0]

#               def ufunc(rst_ndx):
#                   (rst, ndx) = rst_ndx
#                   if [] == rst or num <= ndx: return None
#                   return (rst[1:], (rst[1:], ndx + 1))
#               return util.head_or(lst, unfold_right_i(ufunc, (lst, 0)))
def drop_u(num, lst): return split_at_u(num, lst)[1]

def anyall_u(pred, lst):
    func = lambda acc, e: (acc[0] or pred(e), acc[1] and pred(e))
    def ufunc(acc_rst):
        (acc, rst) = acc_rst
        if [] == rst: return None
        return (func(acc, rst[0]), (func(acc, rst[0]), rst[1:]))
    return util.head_or((False, True), unfold_right_i(ufunc,
        ((False, True), lst)))

def any_u(pred, lst): return anyall_u(pred, lst)[0]

def all_u(pred, lst): return anyall_u(pred, lst)[1]

def map_u(func, lst):
    def ufunc(rst):
        return None if [] == rst else (func(rst[0]), rst[1:])
    #return list(reversed(unfold_right_i(ufunc, lst)))
    return unfold_left_r(ufunc, lst)

def foreach_u(func, lst):
    def ufunc(rst):
        return None if [] == rst else (func(rst[0]), rst[1:])
    #return ([None] + list(reversed(unfold_right_i(ufunc, lst))))[-1]
    return ([None] + unfold_left_r(ufunc, lst))[-1]

def partition_u(pred, lst):
    def gen_func(el, lst0_lst1):
        (lst0, lst1) = lst0_lst1
        return (lst0 + [el], lst1) if pred(el) else (lst0, lst1 + [el])
    def ufunc(wss_zss_rst):
        ((wss, zss), rst) = wss_zss_rst
        if [] == rst: return None
        return (gen_func(rst[0], (wss, zss)),
            (gen_func(rst[0], (wss, zss)), rst[1:]))
    return util.head_or(([], []), unfold_right_i(ufunc, (([], []), lst)))

#   def gen_func(el, acc): return (acc + [el]) if pred(el) else acc
#   def ufunc(acc_rst):
#       (acc, rst) = acc_rst
#       if [] == rst: return None
#       return (gen_func(rst[0], acc), (gen_func(rst[0], acc), rst[1:]))
#   return util.head_or([], unfold_right_i(ufunc, ([], lst)))
def filter_u(pred, lst): return partition_u(pred, lst)[0]

#   def gen_func(el, acc): return (acc + [el]) if not pred(el) else acc
#   def ufunc(acc_rst):
#       (acc, rst) = acc_rst
#       if [] == rst: return None
#       return (gen_func(rst[0], acc), (gen_func(rst[0], acc), rst[1:]))
#   return util.head_or([], unfold_right_i(ufunc, ([], lst)))
def remove_u(pred, lst): return partition_u(pred, lst)[1]


def is_ordered_u(xss, key_func=None, reverse=False):
    if None == key_func: key_func = lambda x: x
    _flip_le = _flip_func(operator.le, reverse)
    #if 1 2 > len(xss): return True
    def ufunc(acc_rst):
        (acc, rst) = acc_rst
        if 2 > len(rst): return None
        return (acc and _flip_le(rst[0], rst[1]),
            (acc and _flip_le(rst[0], rst[1]), rst[1:]))
    return util.head_or(True, unfold_right_i(ufunc, (True, xss)))


def append_u(xss, yss):
    def ufunc(acc_rst):
        (acc, rst) = acc_rst
        if [] == rst: return None
        return (acc + [rst[0]], (acc + [rst[0]], rst[1:]))
    return util.head_or(xss[:], unfold_right_i(ufunc, (xss[:], yss)))

def interleave_u(xss, yss):
    len_short = len(xss) if len(xss) < len(yss) else len(yss)
    init = xss[len_short:] + yss[len_short:]
    def ufunc(acc_wss_rst):
        (acc, wss, rst) = acc_wss_rst
        if [] == rst: return None
        return ([wss[-1], rst[0]] + acc,
            ([wss[-1], rst[0]] + acc, wss[:-1], rst[1:]))
    return util.head_or(init, unfold_right_i(ufunc,
        (init, xss[:len_short], list(reversed(yss[:len_short])))))

def map2_u(func, xss, yss):
    len_short = len(xss) if len(xss) < len(yss) else len(yss)
    def ufunc(rst):
        return None if [] == rst else (func(xss[rst[0]], yss[rst[0]]), rst[1:])
    #return list(reversed(unfold_right_i(ufunc, list(range(len_short)))))
    return unfold_left_r(ufunc, list(range(len_short)))

def zip_u(xss, yss):
    return map2_u(lambda *args: tuple(args), xss, yss)

def unzip_u(ziplst):
    def ufunc(acc_rst):
        (acc, rst) = acc_rst
        if [] == rst: return None
        return ([acc[0] + (rst[0][0],), acc[1] + (rst[0][1],)],
            ([acc[0] + (rst[0][0],), acc[1] + (rst[0][1],)], rst[1:]))
    return util.head_or([(), ()], unfold_right_i(ufunc,
        ([(), ()], ziplst)))

def concat_u(nlsts):
    def ufunc(acc_rst):
        (acc, rst) = acc_rst
        return None if [] == rst else  (rst[0] + acc, (rst[0] + acc, rst[1:]))
    return util.head_or([], unfold_right_i(ufunc,
        ([], list(reversed(nlsts)))))


def tabulate_lc(func, cnt): return [func(i) for i in range(cnt)]

def length_lc(lst):
    return ([0] + [x for x in [0] for e in lst for x in [x + 1]])[-1]

def nth_lc(idx, lst):
    return ([None] + [x for x in [None] for (i, e) in enumerate(lst)
        for x in [e if idx == i else x]])[-1]

def index_find_lc(data, lst, idx=0):
    return ([(-1, None)] + [acc for acc in [(-1, None)] for (i, e) in
        enumerate(lst) for acc in [(i, e) if -1 == acc[0] and 
        data == e else acc]])[-1]

def index_lc(data, lst): return index_find_lc(data, lst)[0]

def find_lc(data, lst): return index_find_lc(data, lst)[1]

def minmax_lc(lst):
    if [] == lst: raise Exception('empty list')
    return ([(lst[0], lst[0])] + [(lo, hi) for (lo, hi) in [(lst[0], lst[0])]
        for e in lst[1:] for (lo, hi) in [(e, hi) if lo > e else (lo, e)
        if hi < e else (lo, hi)]])[-1]

def min_lc(lst): return minmax_lc(lst)[0]

def max_lc(lst): return minmax_lc(lst)[1]

def reverse_lc(lst):
    return ([[]] + [x for x in [[]] for e in lst for x in [[e] + x]])[-1]

def copy_of_lc(lst): return [e for e in lst]

def split_at_lc(num, lst):
    return ([([], [])] + [(at, ad) for (at, ad) in [([], [])]
        for (i, e) in enumerate(lst) for (at, ad) in [(at + [e], ad)
            if num > i else (at, ad + [e])]])[-1]

#            return ([[]] + [a for a in [[]] for (i, e) in enumerate(lst)
#                for a in [a + [e] if num > i else a]])[-1]
def take_lc(num, lst): return split_at_lc(num, lst)[0]

#            return ([[]] + [a for a in [[]] for (i, e) in enumerate(lst)
#                for a in [a + [e] if num <= i else a]])[-1]
def drop_lc(num, lst): return split_at_lc(num, lst)[1]

def anyall_lc(pred, lst):
    func = lambda acc, e: (acc[0] or pred(e), acc[1] and pred(e))
    return ([(False, True)] + [x for x in [(False, True)] for e in lst
        for x in [func(x, e)]])[-1]

def any_lc(pred, lst): return anyall_lc(pred, lst)[0]

def all_lc(pred, lst): return anyall_lc(pred, lst)[1]

def map_lc(func, lst): return [func(e) for e in lst]

def foreach_lc(func, lst): return ([None] + [func(e) for e in lst])[-1]

def partition_lc(pred, lst):
    return ([([], [])] + [(af, ar) for (af, ar) in [([], [])]
        for e in lst for (af, ar) in [(af + [e], ar) if pred(e)
        else (af, ar + [e])]])[-1]

#                       return ([[]] + [a for a in [[]] for e in lst
#                           for a in [a + [e] if pred(e) else a]])[-1]
def filter_lc(pred, lst): return partition_lc(pred, lst)[0]

#                       return ([[]] + [a for a in [[]] for e in lst
#                           for a in [a + [e] if not pred(e) else a]])[-1]
def remove_lc(pred, lst): return partition_lc(pred, lst)[1]


def is_ordered_lc(xss, key_func=None, reverse=False):
    if None == key_func: key_func = lambda x: x
    _flip_le = _flip_func(operator.le, reverse)
    if 2 > len(xss): return True
    return ([(xss[0], True)] + [(old, acc) for (old, acc) in [(xss[0], True)]
        for e in xss[1:] for (old, acc) in
        [(e, acc and _flip_le(old, e))]])[-1][1]


def append_lc(xss, yss):
    return ([xss[:]] + [acc for acc in [xss[:]] for e in yss
        for acc in [acc + [e]]])[-1]

def interleave_lc(xss, yss):
    len_short = len(xss) if len(xss) < len(yss) else len(yss)
    init = xss[len_short:] + yss[len_short:]
    return ([init] + [acc for (wss, acc) in [(xss[:len_short], init)]
        for y in reversed(yss[:len_short])
        for (wss, acc) in [(wss[:-1], [wss[-1], y] + acc)]])[-1]

def map2_lc(func, xss, yss):
    len_short = len(xss) if len(xss) < len(yss) else len(yss)
    return [func(xss[i], yss[i]) for i in range(len_short)]

def zip_lc(xss, yss):
    return map2_lc(lambda *args: tuple(args), xss, yss)

def unzip_lc(ziplst):
    return ([[ah, at] for (ah, at) in [((), ())] for (eh, et) in ziplst
        for (ah, at) in [(ah + (eh,), at + (et,))]])[-1]

def concat_lc(nlsts):
    return ([[]] + [x for x in [[]] for e in reversed(nlsts)
        for x in [e + x]])[-1]


def tabulate_imap(func, cnt, start=0):
    lst_gen = map(func, itertools.count(start))
    return [next(lst_gen) for i in range(cnt)]

def nth_islice(idx, lst, default=None):
    return next(itertools.islice(lst, idx, None), default)

def split_at_islice(num, lst):
    acc_t = list(itertools.islice(lst, num))
    acc_d = list(itertools.islice(lst, num, None))
    return (acc_t, acc_d)

def take_islice(num, lst): return split_at_islice(num, lst)[0]

def drop_islice(num, lst): return split_at_islice(num, lst)[1]

                       # return list(itertools.chain.from_iterable(nlsts))
def concat_chain(nlsts): return list(itertools.chain(*nlsts))
