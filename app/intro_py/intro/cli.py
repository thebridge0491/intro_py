# -*- coding: utf-8 -*-
'''Command line interface module for intro_py-intro.

'''

from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import os, sys, argparse, json
import logging, inspect
from future.builtins import (ascii, filter, hex, map, oct, zip, str, open, dict)

from intro_py import util, intro
from intro_py.intro import person
from intro_py.practice import classic, sequenceops as seqops

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

def run_intro(opts, rsrc_path=None):
    import random, re
    from datetime import datetime

    user1 = {'name': opts['user'], 'num': opts['num'], 
		'time_in': datetime.now()}

    num_arr, num_i, delay_secs = [0b1011, 0o13, 0xb, 11], 0, 2.5

    pers1 = person.Person('I.M. Computer', 32)

    for num in num_arr:
        num_i += num
    assert (len(num_arr) * num_arr[0]) == num_i

    ch = intro.delay_char(delay_secs)

    random.seed()
    if 0 == user1['num']:
        user1['num'] = random.randrange(0, 19)

    rexp = re.compile('(^quit$)', re.I)
    print('{0} match: {1} to {2}'.format('Good' if rexp.match(user1['name'])
        else 'Does not', user1['name'], rexp.pattern))

    greet_str = intro.greeting('greet.txt', user1['name'], rsrc_path=rsrc_path)
    print('{0}\n{1}'.format(user1['time_in'].strftime('%c'), greet_str))

    time_diff = (datetime.now() - user1['time_in']).total_seconds()
    print('(program {0}) Took {1:.1f} seconds.'.format(__name__, time_diff))

    print('#' * 40)

    xss = [2, 3, 1, 4, 0]
    if opts['is_expt2']:
        print('classic.expt_i({0}, {1}): {2}'.format(2.0, float(user1['num']),
            classic.expt_i(2.0, float(user1['num']))))
        print('seqops.reverse_i({0}): {1}'.format(xss, seqops.reverse_i(xss)))
        print('sorted({0}): {1}'.format(xss, sorted(xss)))
    else:
        print('classic.fact_i({0}): {1}'.format(user1['num'],
            classic.fact_i(user1['num'])))
        el = 3
        print('seqops.index_i({0}, {1}): {2}'.format(el, xss,
            seqops.index_i(el, xss)))
        print('{0}.append({1}): '.format(xss, 50), end='')
        xss.append(50)
        print(xss)

    print('#' * 40)
    res_pascaltri = classic.pascaltri_add(5)
    print('classic.pascaltri_add({0}): {0}'.format(5, res_pascaltri))
    for el in res_pascaltri:
        print(el)
    print()

    res_hanoi = classic.hanoi(1, 2, 3, 4)
    print('classic.hanoi(1, 2, 3, 4): {0}'.format(res_hanoi))
    for el in classic.hanoi_moves(4, res_hanoi)[1]:
        print(el)
    print()

    solved_nqueens = classic.nqueens(8)
    queens_ndx = random.randrange(0, len(solved_nqueens))
    res_nqueens = solved_nqueens[queens_ndx]
    print('classic.nqueens(8)[{0}]: {1}'.format(queens_ndx, res_nqueens))
    for el in classic.nqueens_grid(8, res_nqueens):
        print('-'.join(el))
    print()

    print('#' * 40)

    print('pers1.age:', pers1.age)
    pers1.age = 33
    print('str(pers1):', pers1)
    print('repr(pers1):', repr(pers1))

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
    opts_parser.add_argument('-u', '--user', action = 'store', type = str,
        default = 'World', help = 'set name')
    opts_parser.add_argument('-n', '--num', action = 'store', type = int,
        default = 0, help = 'set num')
    opts_parser.add_argument('-2', '--is_expt2', action = 'store_true',
        default = False, help = 'compute expt 2 vice factorial')

    return opts_parser.parse_args(args)

def main(argv=None):
    '''Main entry.

    Args:
        argv (list): list of arguments
    Returns:
        int: A return code
    Demonstrates Python syntax
    '''
    
    rsrc_path = os.environ.get('RSRC_PATH')
    logjson_str = util.read_resource('logging.json', rsrc_path=rsrc_path)
    log_cfg = deserialize_str(logjson_str, fmt='json')
    util.config_logging('info', 'cfg', log_cfg)
    opts_hash = parse_cmdopts(argv)
    util.config_logging(opts_hash.log_lvl, opts_hash.log_opt, log_cfg)
    MODULE_LOGGER.info('main()')

    cfg_blank = {'hostname':'???', 'domain':'???', 'file1':{'path':'???', 
		'ext':'txt'}, 'user1':{'name':'???', 'age': -1}}
    cfg_ini = dict(cfg_blank.items())
    cfg_ini.update(util.ini_to_dict(util.read_resource('prac.conf',
		rsrc_path=rsrc_path)).items())
    #cfg_json = dict(cfg_blank.items())
    #cfg_json.update(deserialize_str(util.read_resource('prac.json',
	#	rsrc_path=rsrc_path)).items())
    #cfg_yaml = dict(cfg_blank.items())
    #cfg_yaml.update(deserialize_str(util.read_resource('prac.yaml',
	#	rsrc_path=rsrc_path), fmt='yaml').items())
    #cfg_toml = dict(cfg_blank.items())
    #cfg_toml.update(deserialize_str(util.read_resource('prac.toml',
	#	rsrc_path=rsrc_path), fmt='toml').items())
    
    tup_arr = [
        (cfg_ini, cfg_ini['domain'], cfg_ini['user1']['name'])
        #, (cfg_json, cfg_json['domain'], cfg_json['user1']['name'])
        #, (cfg_yaml, cfg_yaml['domain'], cfg_yaml['user1']['name'])
        #, (cfg_toml, cfg_toml['domain'], cfg_toml['user1']['name'])
    ]
    
    for (cfg, domain, user1Name) in tup_arr:
        print('\nconfig: {0}'.format(cfg))
        print('domain: {0}'.format(domain))
        print('user1Name: {0}'.format(user1Name))
    print('')
    run_intro(vars(opts_hash), rsrc_path=rsrc_path)

    logging.shutdown()
    return 0

if '__main__' == __name__:
    sys.exit(main(sys.argv[1:]))
