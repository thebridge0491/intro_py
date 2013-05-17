# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import sys, os, re, unittest
from future.builtins import (ascii, filter, hex, map, oct, zip)

__all__ = ['main']


HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(HERE)

def main(test_names=None):
    import pkgutil
    
    if not test_names:
        test_names = []
        #for name in ['test_new']:
        #    test_names.append(name)
        for _, name, _ in pkgutil.iter_modules([os.path.dirname(__file__)]):
            test_names.append(name)
    
    suite = unittest.TestSuite()
    for name in test_names:
        str2 = re.search('^(test_[a-z_]+)', name)
        if str2:
            try:
                suite.addTest(unittest.TestLoader().loadTestsFromName(name))
            except unittest.SkipTest as exc:
                print('###{0}###: {1}'.format(__name__, repr(exc)))
    unittest.TextTestRunner(verbosity = 2).run(suite)
    return 0


#if '__main__' == __name__:
#    raise SystemExit(main(sys.argv[1:]))
