# -*- coding: utf-8 -*-
'''Library functions module

'''

from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import sys, logging
from future.builtins import (ascii, filter, hex, map, oct, zip, str)

from intro_py.foreignc import classic

__all__ = []


MODULE_LOGGER = logging.getLogger(__name__)


def lib_main(argv=None):
    print('fact_i(5):', classic.fact_i(5))
    return 0

if '__main__' == __name__:
    sys.exit(lib_main(sys.argv[1:]))
