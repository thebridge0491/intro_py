# -*- coding: utf-8 -*-
'''Library functions module

'''

from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import sys, os, logging
from future.builtins import (ascii, filter, hex, map, oct, zip, str)

__all__ = ['read_resource', 'config_logging', 'ini_to_dict', 'in_epsilon', 
    'cartesian_prod', 'bound_values', 'robust_values', 'robust_failures',
    'worst_values', 'worst_failures', 'head_or', 'last_or']


MODULE_LOGGER = logging.getLogger(__name__)

def read_resource(filepath, pkg_or_mod=__name__, rsrc_path=None):
	import pkgutil #, pkg_resources
	try:
		if rsrc_path is None:
			#output = pkg_resources.resource_string(pkg_or_mod, 'resources/' + filepath)
			output = pkgutil.get_data(pkg_or_mod, 'resources/' + filepath)
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

def ini_to_dict(ini_str):
    import re
    
    try:
        from configparser import SafeConfigParser
    except ImportError:
        from ConfigParser import SafeConfigParser
    finally:
        config, conf_dict = SafeConfigParser(), {}
        config.optionxform = str
        try:
            config.read_string(ini_str.decode(encoding='utf-8'))
        except AttributeError:
            from io import StringIO
            config.readfp(StringIO(ini_str.decode(encoding='utf-8')))

    for sect in config.sections():
        if 'default' != sect:
            conf_dict[sect] = tmp_dict = {}
        else:
            tmp_dict = conf_dict
        for key, val in config.items(sect):
            match_1 = re.search('([^#]*)', val)
            tmp_dict[key] = match_1.groups()[0].strip().strip("'")
    return conf_dict

def in_epsilon(val_a, val_b, tolerance=0.001):
    #return ((abs(val_a) - tolerance) <= abs(val_b) and
    #    (abs(val_a) + tolerance) >= abs(val_b))
    delta = abs(tolerance)
    #return (val_a - delta) <= val_b and (val_a + delta) >= val_b
    return (not (val_a + delta) < val_b) and (not (val_b + delta) < val_a)

def cartesian_prod(xs, ys):
    return [(x, y) for x in xs for y in ys]

def bound_values(*min_max_groups):
    '''Create analysis set of boundary(4n+1) values.'''
    avg_vals = [(min_m + max_m) // 2 for (min_m, max_m) in min_max_groups]
    axis_bounds = [(min_m, min_m + 1, (min_m + max_m) // 2, max_m - 1, max_m)
        for (min_m, max_m) in min_max_groups]
    bound_vals = [tuple(avg_vals[:ndx] + [el] + avg_vals[(ndx + 1):])
        for ndx, axis in enumerate(axis_bounds) for el in axis]
    return set(bound_vals)

def robust_failures(*min_max_groups):
    '''Create addon set of robustness(2n) values.'''
    avg_vals = [(min_m + max_m) // 2 for (min_m, max_m) in min_max_groups]
    axis_robusts = [(min_m - 1, max_m + 1)
        for (min_m, max_m) in min_max_groups]
    addon_vals = [tuple(avg_vals[:ndx] + [el] + avg_vals[(ndx + 1):])
        for ndx, axis in enumerate(axis_robusts) for el in axis]
    return set(addon_vals)

def robust_values(*min_max_groups):
    '''Create analysis set of robustness(6n+1) values.'''
    return bound_values(*min_max_groups) | robust_failures(*min_max_groups)

def worst_values(*min_max_groups):
    '''Create analysis set of worst-case(5**n) values.'''
    # import itertools

    axis_worsts = [(min_m - 1, min_m, (min_m + max_m) // 2, max_m, max_m + 1)
        for (min_m, max_m) in min_max_groups]
    # return set(itertools.product(*axis_worsts))

    def iter(rst, acc):
        if 0 >= len(rst):
            return acc
        res = [el0 + (el1,) for el0 in acc for el1 in rst[0]]
        return iter(rst[1:], res)
    tmp_vals = [(el0,) for el0 in axis_worsts[0]]
    if 2 > len(min_max_groups):
        worst_vals = tmp_vals
    else:
        worst_vals = iter(axis_worsts[1:], tmp_vals)
    return set(worst_vals)

def worst_failures(*min_max_groups):
    '''Create failure set of worst-case(5**n - 3**n) values.'''
    import itertools

    axis_passes = [(min_m, (min_m + max_m) // 2, max_m)
        for (min_m, max_m) in min_max_groups]
    worst_passes = set(itertools.product(*axis_passes))
    return worst_values(*min_max_groups) - worst_passes

def head_or(null_default, lst):
    return null_default if [] == lst else lst[0]

def last_or(null_default, lst):
    return null_default if [] == lst else lst[-1]


def lib_main(argv=None):
    print('cartesian_prod([0, 1, 2], [10, 20, 30]):',
        cartesian_prod([0, 1, 2], [10, 20, 30]))
    return 0

if '__main__' == __name__:
    sys.exit(lib_main(sys.argv[1:]))
