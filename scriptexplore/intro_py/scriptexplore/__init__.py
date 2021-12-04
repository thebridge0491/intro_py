# -*- coding: utf-8 -*-
'''Script explore sub-package for Python Intro examples project.'''
#from __future__ import (absolute_import, unicode_literals)

import os, sys, logging

_dict_metadata = {}
try:
    if sys.version_info >= (3, 8):
        from importlib import metadata
    else:
        import importlib_metadata as metadata
    _dict_metadata = metadata.metadata('intro_py.scriptexplore')
except (ImportError, NameError) as exc:
    print(repr(exc))

# add {wheel,egg,jar}/site-packages to sys.path
if __package__ in ['', None]:
    path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    sys.path.extend([os.path.join(path, 'site-packages')])

from .lib import *


# PEP 566 -- Metadata for Python Software Packages 2.1
#__version__ = metadata.version('intro_py.scriptexplore')
__version__ = _dict_metadata.get('Version', '0.0.0')
__date__ = '2013-05-06'
__author__ = '{0} <{1}>'.format(_dict_metadata.get('Author', 'imcomputer'),
    _dict_metadata.get('Author-email', 'imcomputer-codelab@yahoo.com'))
__credits__ = '; '.join(map(str, [_dict_metadata.get('Author', 'imcomputer')]))
__license__ = _dict_metadata.get('License', 'Apache-2.0')
__copyright__ = '(c) {0}, {1}'.format(__date__.split('-')[0],
    _dict_metadata.get('Author', 'imcomputer'))

logging.getLogger(__name__).addHandler(logging.NullHandler())
