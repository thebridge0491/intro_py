# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys

if '__main__' == __name__:
    def parse_cmdopts(args=None):
        import argparse
        opts_parser = argparse.ArgumentParser()
        
        opts_parser.add_argument('-m', '--main', action = 'store_true',
            default = False, help = 'Run main app vice test main')
        opts_parser.add_argument('rest', nargs=argparse.REMAINDER)
        
        return opts_parser.parse_args(args)
 
    opts_hash = parse_cmdopts(sys.argv[1:])
    
    if opts_hash.main:
        from intro_py.util import cli
        sys.exit(cli.main(opts_hash.rest[1:]))
    else:
        from intro_py.util.tests import ts_main
        sys.exit(ts_main.main(opts_hash.rest[1:]))
