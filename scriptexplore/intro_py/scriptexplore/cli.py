# -*- coding: utf-8 -*-
'''Command line interface module for intro_py-scriptexplore.

'''

from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import os, sys, argparse, json
import logging, inspect
#from builtins import (ascii, filter, hex, map, oct, zip, str, open, dict)

from intro_py import scriptexplore

__all__ = ['main']

# -- run w/out compile --
# python script.py [arg1 argN]
# 
# -- run REPL, import script, & run --
# python
# >>> from . import script.py
# >>> script.main([arg1, argN])
# 
# -- help/info tools in REPL --
# help(), quit(), help(<object>), help([modules|keywords|symbols|topics])
# 
# -- show module/type info --
# ex: pydoc list OR python> help(list)


logging.basicConfig(level = logging.DEBUG)
MODULE_LOGGER = logging.getLogger(__name__)

def deserialize_str(str1, fmt='json'):
	if str1 is not None:
		if 'json' == fmt:
			return json.loads(str1)
		elif 'yaml' == fmt:
			try:
				import yaml
				return yaml.load(str1)
			except ImportError as exc:
				print(repr(exc))
		elif 'toml' == fmt:
			try:
				import toml
				return toml.loads(str1)
			except ImportError as exc:
				print(repr(exc))
	return {}

def parse_cmdopts(args=None):
    func_name = inspect.stack()[0][3]
    MODULE_LOGGER.info(func_name + '()')

    opts_parser = argparse.ArgumentParser()

    opts_parser.add_argument('-v', '--log_lvl', action = 'store',
        default = None, choices = [None, 'debug', 'info', 'warning', 'error',
        'critical'], dest = 'log_lvl', help = 'Set logging level')
    opts_parser.add_argument('-l', '--log', action = 'store', type = str,
        default = 'cfg', choices = [None, 'basic', 'cfg'],
        dest = 'log_opt', help = 'Set logging config')
    #opts_parser.add_argument('-S', '--simple', action = 'store_true',
    #    default = False, help = 'select simple module')
    opts_parser.add_argument('-m', '--mod', action = 'store', type = str,
        default = 'simple', choices = [None, 'simple', 'advanced', 'mymd5',
        'ggrep', 'ddiff'], dest = 'mod', help = 'select run module')
    opts_parser.add_argument('rest', nargs=argparse.REMAINDER)

    return opts_parser.parse_args(args)

def main(argv=None):
    '''Main entry.

    Args:
        argv (list): list of arguments
    Returns:
        int: A return code
    Demonstrates Python syntax
    '''
    
    import importlib
    
    os.environ.setdefault('PATH_PFX', 'intro_py/scriptexplore/resources/explore')
    rsrc_path = os.environ.get('RSRC_PATH')
    logjson_str = scriptexplore.read_resource('logging.json', rsrc_path=rsrc_path)
    log_cfg = deserialize_str(logjson_str, fmt='json')
    scriptexplore.config_logging('info', 'cfg', log_cfg)
    opts_hash = parse_cmdopts(argv)
    scriptexplore.config_logging(opts_hash.log_lvl, opts_hash.log_opt, log_cfg)
    MODULE_LOGGER.info('main()')
    
    #if opts_hash.simple:
    #    from intro_py.scriptexplore import simple
    #    runmod = simple
    runmod = importlib.import_module('intro_py.scriptexplore.' + opts_hash.mod)
    
    runmod.main(opts_hash.rest) if [] != opts_hash.rest else runmod.main()
    
    logging.shutdown()
    return 0

if '__main__' == __name__:
    sys.exit(main(sys.argv[1:]))
