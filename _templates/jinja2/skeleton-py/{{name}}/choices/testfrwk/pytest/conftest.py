# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import os, logging, json
from future.builtins import (ascii, filter, hex, map, oct, zip, str)

from {{parent}} import {{project}}


def addoption_pytest(parser, hypo_cfg0):
    parser.addoption('--log', action = 'store', type = str,
        default = None, choices = ['basic', 'cfg'],
        dest = 'log_opt', help = 'Set logging config')
    parser.addoption('--log-lvl', action = 'store', type = str,
        default = None, choices = ['debug', 'info', 'warning', 'error',
        'critical'], dest = 'log_lvl', help = 'Set logging level')
    
    try:
        import hypothesis
    except ImportError as exc:
        print(repr(exc))
        return
    hypo_cfg = {'max_examples': '200', 'max_iterations': '1000',
        'timeout': '60', 'verbosity': 'normal'}
    hypo_cfg.update(hypo_cfg0 if hypo_cfg0 is not None else {})
    parser.addoption('--max', action = 'store', type = int,
        default = int(hypo_cfg['max_examples']),
        help = 'Set max_examples for hypothesis')
    parser.addoption('--iter', action = 'store', type = int,
        default = int(hypo_cfg['max_iterations']),
        help = 'Set max_iterations for hypothesis')
    parser.addoption('--timeout-hypo', action = 'store', type = int,
        default = int(hypo_cfg['timeout']), dest = 'timeout_hypo',
        help = 'Set timeout for hypothesis')
    parser.addoption('--verbose-hypo', action = 'store', type = str,
        default = hypo_cfg['verbosity'], dest = 'verbose_hypo',
        choices = ['quiet', 'normal', 'verbose', 'debug'],
        help = 'Set verbosity for hypothesis')

def configure_pytest(config, log_cfg):
    {{project}}.config_logging(config.getoption('--log-lvl'),
        config.getoption('--log'), log_cfg)
    logging.info('conftest.py: pytest_configure()')

    try:
        import os
        from hypothesis import settings, Verbosity
    except ImportError as exc:
        print(repr(exc))
        return
    # settings.database_file = '.hypothesis/examples'
    # os.environ['HYPOTHESIS_DATABASE_FILE'] = '.hypothesis/examples'
    os.environ['HYPOTHESIS_STORAGE_DIRECTORY'] = '.hypothesis'
    settings.register_profile('cmdln', settings(verbosity = getattr(
        Verbosity, config.getoption('--verbose-hypo').lower(),
        Verbosity.verbose),
        max_examples = config.getoption('--max'),
        max_iterations = config.getoption('--iter'),
        timeout = config.getoption('--timeout-hypo')))

    # settings.load_profile(os.getenv(u'HYPOTHESIS_PROFILE', 'default'))

def pytest_addoption(parser):
	rsrc_path = os.environ.get('RSRC_PATH')
	hypojson_str = {{project}}.read_resource('hypothesis.json', rsrc_path=rsrc_path)
    hypo_cfg = json.loads(json_bytes.decode(encoding='utf-8')) if hypojson_str is not None else {}
    addoption_pytest(parser, hypo_cfg)

def pytest_configure(config):
	rsrc_path = os.environ.get('RSRC_PATH')
	logjson_str = {{project}}.read_resource('logging.json', rsrc_path=rsrc_path)
    log_cfg = json.loads(json_bytes.decode(encoding='utf-8')) if logjson_str is not None else {}
    configure_pytest(config, log_cfg)
