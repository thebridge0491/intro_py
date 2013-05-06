# -*- coding: utf-8 -*-
'''Entrypoint module, in case you use `python -m {{parent}}.{{project}}`.'''

import sys

from {{parent}}.{{project}} import cli

if '__main__' == __name__:
    cli.main(sys.argv[1:])
