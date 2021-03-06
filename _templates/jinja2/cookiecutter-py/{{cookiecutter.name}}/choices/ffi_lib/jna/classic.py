# -*- coding: utf-8 -*-
'''Classic module.

'''

from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import os, sys, logging, inspect, glob
from future.builtins import (ascii, filter, hex, map, oct, zip)

from java.lang import Long as JLong, Float as JFloat
import jarray

try:
    # jip install net.java.dev.jna:jna:X.Y.Z --> javalib/jna*.jar
    # java -jar ivy.jar -dependency net.java.dev.jna jna '[X.Y,)' -types jar -retrieve 'javalib/[artifact]-[revision](-[classifier]).[ext]'
    sys.path.extend(glob.glob('javalib/jna*.jar'))
    from com.sun.jna import NativeLibrary
except Exception as exc:
    raise Exception('Possibly missing javalib/jna*.jar -- check javalib directory.\n' +
        repr(exc))

__all__ = ['fact_i', 'fact_lp', 'expt_i', 'expt_lp']


MODULE_LOGGER = logging.getLogger(__name__)

ffi_jna = NativeLibrary.getInstance('intro_c-practice')

_fact_i = ffi_jna.getFunction('fact_i')
_fact_lp = ffi_jna.getFunction('fact_lp')

_expt_i = ffi_jna.getFunction('expt_i')
_expt_lp = ffi_jna.getFunction('expt_lp')

def fact_i(num):
    func_name = inspect.stack()[0][3]
    MODULE_LOGGER.info(func_name + '()')
    return _fact_i.invoke(JLong, jarray.array([num], JLong))
def fact_lp(num):
    return _fact_lp.invoke(JLong, jarray.array([num], JLong))

def expt_i(base, num):
    return _expt_i.invoke(JFloat, jarray.array([base, num], JFloat))
def expt_lp(base, num):
    return _expt_lp.invoke(JFloat, jarray.array([base, num], JFloat))


def lib_main(argv=None):
    print('fact(5):', fact_i(5))
    return 0

if '__main__' == __name__:
    sys.exit(lib_main(sys.argv[1:]))
