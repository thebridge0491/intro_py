# -*- coding: utf-8 -*-
'''Library functions module

'''

from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import os, sys, logging, inspect
from future.builtins import (ascii, filter, hex, map, oct, zip, str, open)

from intro_py import util

__all__ = ['greeting', 'delay_char']


MODULE_LOGGER = logging.getLogger(__name__)

def greeting(greet_file, name, rsrc_path=None):
    func_name = inspect.stack()[0][3]
    MODULE_LOGGER.info(func_name + '()')
    res_str = util.read_resource(greet_file, rsrc_path=rsrc_path).strip()

    return '{0} {1}!'.format(res_str, name)

def delay_char(delay_secs):
    import time

    ch = ''
    while True:
        time.sleep(delay_secs)
        try:
            ch = input('Type any character when ready.')
        except:
            ch = raw_input('Type any character when ready.')
        if '\n' != ch and '' != ch:
            break
    return str(ch)[0]


def lib_main(argv=None):
    print('delay_char(3):', delay_char(3))
    return 0

if '__main__' == __name__:
    sys.exit(lib_main(sys.argv[1:]))
