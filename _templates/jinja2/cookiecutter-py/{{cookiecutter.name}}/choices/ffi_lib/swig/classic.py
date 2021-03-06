# -*- coding: utf-8 -*-
'''Classic module.

'''

from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import sys, logging, inspect
from future.builtins import (ascii, filter, hex, map, oct, zip)

from {{cookiecutter.parent}}.{{cookiecutter.project}} import classic_c

__all__ = ['fact_i', 'fact_lp', 'expt_i', 'expt_lp']


MODULE_LOGGER = logging.getLogger(__name__)

fact_i = classic_c.fact_i
fact_lp = classic_c.fact_lp

expt_i = classic_c.expt_i
expt_lp = classic_c.expt_lp


def lib_main(argv=None):
    print('fact(5):', fact_i(5))
    return 0

if '__main__' == __name__:
    sys.exit(lib_main(sys.argv[1:]))
