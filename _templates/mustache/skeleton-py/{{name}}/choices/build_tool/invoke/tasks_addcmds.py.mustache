# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

import os, sys, glob, pkg_resources
from invoke import task, tasks
from invoke.util import log

__all__ = ['checker', 'report', 'bdist_jar', 'copyreqs', 'zipreqs'
    ]


os.environ['ZIPOPTS'] = '-9 -q --exclude @{0}/exclude.lst'.format(os.getcwd())

def _browser_py(path):
    import webbrowser
    try:
        from urllib.request import pathname2url
    except:
        from urllib import pathname2url
    webbrowser.open('file://' + pathname2url(os.path.abspath(path)))

def _matches_filepatterns(filepats, paths):
    import fnmatch
    matches_pats = [os.path.join(root, file1) for path in paths
        for root, dirs, files in os.walk(path) for filepat in filepats
        for file1 in fnmatch.filter(dirs + files, filepat)]
    return matches_pats
    
def _remove_pathlist(pathlist):
    import shutil
    for path in pathlist:
        if os.path.exists(path) and os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.exists(path):
            os.remove(path)

@task(help={'check-cmd': 'Checker cmd: choices [pychecker, pylint, flake8, pep8, pep257]'})
def checker(ctx, check_cmd='pychecker', opts=''):
    '''checker - Checker (default: pychecker).'''
    cmds_dict = {'pychecker': 'pychecker.checker',
        'pylint': 'pylint --rcfile setup.cfg', 'flake8': 'flake8',
        'pep8': 'pep8', 'pep257': 'pep257'}
    matches_wout_main = [file1 for file1 in _matches_filepatterns(
        ['*.py'], ['/'.join(ctx.proj_name.split('.')[:-1]), 'tests']) if '__main__.py' not in file1]
    ctx.run('{0} -m {1} {2} {3}'.format(sys.executable,
        cmds_dict.get(check_cmd, 'pychecker.checker'), opts,
        ' '.join(matches_wout_main)), shell='/bin/sh')

@task(help={'rpt-type': 'Report type: choices [report, html, xml]'})
def report(ctx, rpt_type='report', opts=''):
    '''report - report code coverage (default: report).'''
    ctx.run('{0} -m coverage combine'.format(sys.executable), warn=True,
        shell='/bin/sh')
    ctx.run('{0} -m coverage {1} {2}'.format(sys.executable, rpt_type, opts), 
        warn=True, shell='/bin/sh')
    if 'html' == rpt_type and os.path.exists('htmlcov/index.html'):
        ctx.run('w3m -M htmlcov/index.html', shell='/bin/sh')
        #_browser_py('htmlcov/index.html')


@task
def bdist_jar(ctx):
    '''bdist_jar - create jar distribution.'''
    VERSION = pkg_resources.get_distribution(ctx.proj_name)._version
    ctx.run('echo Class-Path: . > build/manifest.mf', shell='/bin/sh')
    ctx.run('jar -cfme dist/{0}-{1}.jar build/manifest.mf org.python.util.JarRunner {0}.*'.format(
        ctx.proj_name, VERSION), shell='/bin/sh')
    ctx.run('zip {0} -r dist/{1}-{2}.jar .'.format(os.environ.get('ZIPOPTS', 
        ''), ctx.proj_name, VERSION), shell='/bin/sh')

@task
def copyreqs(ctx):
    '''copyreqs - copy requirements to build/pylib.'''
    ctx.run('{0} -m pip install -I -t build/pylib/site-packages -r requirements.txt'.format(
        sys.executable), shell='/bin/sh')
    ctx.run('{0} -m pip install -U -I --no-deps -t build/pylib -r requirements-internal.txt'.format(
        sys.executable), shell='/bin/sh')
    _remove_pathlist(glob.glob('build/pylib/**/*-info'))

@task
def zipreqs(ctx):
    '''zipreqs - zip requirements to [wheel|jar] distribution.'''
    cwd = os.getcwd()
    DISTROS = ' '.join(glob.glob('{0}/dist/{1}*.whl'.format(cwd,
        ctx.proj_name)) + glob.glob('{0}/dist/{1}*.jar'.format(cwd,
        ctx.proj_name)))
    ctx.run('for archive in {3} ; do \
                cd {0}/build/pylib ; zip {2} -r $archive * ; \
                zip {2} -d $archive site-packages/copyreg\* ; \
                cd {0}/{1}/tests ; \
                zip {2} -r $archive __main__.py ; \
            done'.format(cwd, ctx.proj_name.replace('.', '/'),
            os.environ.get('ZIPOPTS', ''), DISTROS),
        shell='/bin/sh')
