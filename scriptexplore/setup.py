#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import os, sys, pkg_resources, setuptools, glob

pkg_resources.require('setuptools>=48.0')

HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.extend([HERE, os.path.join(HERE, '..')])


if __name__ == '__main__':
    # enable running setup.py from another directory
    HERE and os.chdir(HERE)
    
    # setuptools modified/add-on cmds
    cmds_addon = {}
    
    try:
        import setup_addcmds
        cmds_addon.update(setup_addcmds.cmdclass)
    except (ImportError, NameError) as exc:
        print(repr(exc))
    if '1' == os.environ.get('DEBUG', '0').lower():
        sys.executable = '{0} -m coverage run'.format(sys.executable)
    setuptools.setup(
        # setuptools modified/add-on cmds
        cmdclass=dict(dict({}) | cmds_addon.items())
    )
