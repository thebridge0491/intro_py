# -*- coding: utf-8 -*-
'''Classic module

'''

from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import sys, logging, inspect
from future.builtins import (ascii, filter, hex, map, oct, zip, str)

__all__ = ['fact_i', 'fact_r', 'fact_lp', 'expt_i', 'expt_r', 'expt_lp']


MODULE_LOGGER = logging.getLogger(__name__)

def fact_i(num):
    func_name = inspect.stack()[0][3]
    MODULE_LOGGER.info(func_name + '()')
    #
    def iter(cnt, acc):
        return acc if 0 >= cnt else iter(cnt - 1, cnt * acc)
    return iter(num, 1)

def fact_r(num):
    return 1 if 1 > num else num * fact_r(num - 1)

def fact_lp(num):
    acc = 1
    for i in range(1, num + 1):
        acc *= i
    return acc

def expt_i(base, num):
    def iter(cnt, acc):
        return acc if 0 >= cnt else iter(cnt - 1, base * acc)
    return iter(int(num), 1.0)

def expt_r(base, num):
    return 1.0 if 0 >= num else base * expt_r(base, num - 1)

def expt_lp(base, num):
    acc = 1.0
    for i in range(0, int(num)):
        acc *= base
    return acc


def lib_main(argv=None):
    print('fact(5):', fact_i(5))
    return 0

if '__main__' == __name__:
    sys.exit(lib_main(sys.argv[1:]))
