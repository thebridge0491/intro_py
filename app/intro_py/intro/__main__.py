# -*- coding: utf-8 -*-
'''Entrypoint module, in case you use `python -m intro_py.intro`.'''

import sys

from intro_py.intro import cli

if '__main__' == __name__:
    cli.main(sys.argv[1:])
