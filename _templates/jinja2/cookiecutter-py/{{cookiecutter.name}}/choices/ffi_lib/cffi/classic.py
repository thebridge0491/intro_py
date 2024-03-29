# -*- coding: utf-8 -*-
'''Classic module.

'''

from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import sys, logging, inspect
from future.builtins import (ascii, filter, hex, map, oct, zip)

from {{cookiecutter.parent}}.{{cookiecutter.project}} import _classic
from {{cookiecutter.parent}}.{{cookiecutter.project}}._classic import lib

__all__ = ['fact_i', 'fact_lp', 'expt_i', 'expt_lp']


MODULE_LOGGER = logging.getLogger(__name__)

def fact_i(num):
    func_name = inspect.stack()[0][3]
    MODULE_LOGGER.info(func_name + '()')
    return lib.fact_i(num)
def fact_lp(num):
    return lib.fact_lp(num)

def expt_i(base, num):
    return lib.expt_i(base, num)
def expt_lp(base, num):
    return lib.expt_lp(base, num)


def lib_main(argv=None):
    print('fact(5):', fact_i(5))
    return 0

if '__main__' == __name__:
    sys.exit(lib_main(sys.argv[1:]))
