# -*- coding: utf-8 -*-
'''Entrypoint module, in case you use `python -m {{cookiecutter.parent}}.{{cookiecutter.project}}`.'''

import sys

from {{cookiecutter.parent}}.{{cookiecutter.project}} import cli

if '__main__' == __name__:
    cli.main(sys.argv[1:])
