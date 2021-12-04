# -*- coding: utf-8 -*-
'''Classic module.

'''

from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import sys, logging, inspect
from ctypes import (CDLL, cdll, c_uint, c_ulong, c_float)
#from builtins import (ascii, filter, hex, map, oct, zip)

__all__ = ['fact_i', 'fact_lp', 'expt_i', 'expt_lp']


MODULE_LOGGER = logging.getLogger(__name__)

# cdll.LoadLibrary("libintro_c-practice.so")
_classic = CDLL("libintro_c-practice.so")

_classic.fact_i.argtypes = _classic.fact_lp.argtypes = [c_uint]
_classic.fact_i.restype = _classic.fact_lp.restype = c_ulong

_classic.expt_i.argtypes = _classic.expt_lp.argtypes = \
    [c_float, c_float]
_classic.expt_i.restype = _classic.expt_lp.restype = c_float

# fact_i = _classic.fact_i

def fact_i(num):
    func_name = inspect.stack()[0][3]
    MODULE_LOGGER.info(func_name + '()')
    return _classic.fact_i(num)
def fact_lp(num):
    return _classic.fact_lp(num)

def expt_i(base, num):
    return _classic.expt_i(base, num)
def expt_lp(base, num):
    return _classic.expt_lp(base, num)


def lib_main(argv=None):
    print('fact(5):', fact_i(5))
    return 0

if '__main__' == __name__:
    sys.exit(lib_main(sys.argv[1:]))
