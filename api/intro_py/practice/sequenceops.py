# -*- coding: utf-8 -*-
'''Sequence operations module

'''

from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import sys, logging, inspect
from future.builtins import (ascii, filter, hex, map, oct, zip, range)

__all__ = ['index_i', 'index_lp', 'reverse_i', 'reverse_r', 'reverse_lp',
    'copy_of_i', 'copy_of_r', 'copy_of_lp']


MODULE_LOGGER = logging.getLogger(__name__)

def swap(idx0, idx1, lst):
    lst[idx0], lst[idx1] = lst[idx1], lst[idx0]

def index_i(data, lst):
    def iter(idx, rst):
        if [] == rst: return -1
        elif data == rst[0]: return idx
        else: return iter(idx + 1, rst[1:])
    return iter(0, lst)

def index_lp(data, lst):
    for i in range(0, len(lst)):
        if data == lst[i]: return i
    return -1

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


def lib_main(argv=None):
    print('index(3, [4, 2, 0, 1, 3]):', index_i(3, [4, 2, 0, 1, 3]))
    return 0

if '__main__' == __name__:
    sys.exit(lib_main(sys.argv[1:]))
