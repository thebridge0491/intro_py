# -*- coding: utf-8 -*-
'''Entrypoint module, in case you use `python -m intro_py.scriptexplore`.'''

import sys

from intro_py.scriptexplore import cli

if '__main__' == __name__:
    cli.main(sys.argv[1:])
