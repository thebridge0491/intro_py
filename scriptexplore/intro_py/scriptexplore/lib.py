# -*- coding: utf-8 -*-
'''Library functions module

'''

from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import sys, os, logging
from future.builtins import (ascii, filter, hex, map, oct, zip, str)

__all__ = ['read_resource', 'config_logging', 'in_epsilon']


MODULE_LOGGER = logging.getLogger(__name__)

def read_resource(filepath, pkg_or_mod=__name__, rsrc_path=None):
	import pkgutil #, pkg_resources
	try:
		if rsrc_path is None:
			#output = pkg_resources.resource_string(pkg_or_mod, 'resources/' + filepath)
			output = pkgutil.get_data(pkg_or_mod, 'resources/' + filepath
				).decode(encoding='utf-8')
		else:
			with open(os.path.join(rsrc_path, filepath)) as fIn:
				output = fIn.read()
	except IOError as exc:
		print(repr(exc), filepath)
		output = None
	return output

def config_logging(log_lvl=None, log_opt=None, log_dict=None,
        mod_logger=logging.root):
    import logging.config

    log_cfg = {"version": 1}
    log_cfg.update(log_dict if log_dict is not None else {})
    use_log = True if log_lvl is not None or log_opt is not None else False
    if use_log and log_opt and 'cfg' == log_opt.lower():
        logging.config.dictConfig(log_cfg)
    elif use_log:
        logging.basicConfig()
    if use_log and log_lvl:
        for hdlr in mod_logger.handlers:
            hdlr.setLevel(getattr(logging, log_lvl.upper(), None))
        mod_logger.setLevel(getattr(logging, log_lvl.upper(), None))

def in_epsilon(val_a, val_b, tolerance=0.001):
    #return ((abs(val_a) - tolerance) <= abs(val_b) and
    #    (abs(val_a) + tolerance) >= abs(val_b))
    delta = abs(tolerance)
    #return (val_a - delta) <= val_b and (val_a + delta) >= val_b
    return (not (val_a + delta) < val_b) and (not (val_b + delta) < val_a)


def lib_main(argv=None):
    print('in_epsilon(3.0, 3.01, 0.001):', in_epsilon(3.0, 3.01, 0.001))
    print('in_epsilon(3.00, 3.001, 0.001):', in_epsilon(3.00, 3.001, 0.001))
    return 0

if '__main__' == __name__:
    sys.exit(lib_main(sys.argv[1:]))
