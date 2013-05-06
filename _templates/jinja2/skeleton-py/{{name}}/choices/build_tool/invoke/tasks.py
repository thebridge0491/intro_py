# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

import os, sys
from invoke import task, tasks
from invoke.util import log

__all__ = ['help', 'build', 'clean', 'test', 'develop', 'install', 
    'bdist_wheel', 'sdist', 'build_sphinx'
    ]


HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.extend([os.path.join(HERE, '..')])

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

@task(default=True)
def help(ctx):
    '''help - help on project's invoke tasks.'''
    print('Usage: [DEBUG=1] {0} -m invoke [task].'.format(sys.executable))
    ctx.run('{0} -m invoke --list'.format(sys.executable), shell='/bin/sh')

@task
def build(ctx, opts=''):
    '''build - build artifacts.'''
    ctx.run('{0} setup.py build {1}'.format(sys.executable, opts), pty=True,
        shell='/bin/sh')
#    ctx.run('{0} setup.py --name'.format(sys.executable), pty=True,
#        shell='/bin/sh')
    print(ctx.proj_name)

@task
def clean(ctx, opts=''):
    '''clean - remove build artifacts.'''
    from invoke.util import enable_logging
    enable_logging()
    ctx.run('{0} setup.py clean {1}'.format(sys.executable, opts), pty=True,
        shell='/bin/sh')
    if opts in ['-a', '--all']:
        _remove_pathlist(_matches_filepatterns(['build', 'dist', '*.egg*',
            '.cache', '__pycache__', '.hypothesis', 'htmlcov', '.tox', '*.so',
            '*.pyc', '*.pyo', '*~', '.coverage*', '*.log', '*.class'], ['.']))
    log.info('cleaned up')

@task
def test(ctx, opts=''):
    '''test - test package [DEBUG=1].'''
    ctx.run('{0} setup.py test {1}'.format(sys.executable, opts), pty=True, 
        warn=True, shell='/bin/sh')

@task
def develop(ctx, opts='.'):
    '''develop - install package in 'development mode'.'''
    ctx.run('{0} setup.py develop {1}'.format(sys.executable, opts), pty=True,
        shell='/bin/sh')

@task
def install(ctx, opts=''):
    '''install - install package.'''
    ctx.run('{0} setup.py install {1}'.format(sys.executable, opts), pty=True,
        shell='/bin/sh')

@task
def bdist_wheel(ctx, opts=''):
    '''bdist_wheel - create wheel distribution.'''
    ctx.run('{0} setup.py bdist_wheel {1}'.format(sys.executable, opts),
        pty=True, shell='/bin/sh')

@task
def sdist(ctx, opts=''):
    '''sdist - create source distribution.'''
    ctx.run('{0} setup.py sdist {1}'.format(sys.executable, opts), pty=True,
        shell='/bin/sh')

@task(aliases=['docs'])
def build_sphinx(ctx, opts=''):
    '''build_sphinx - build Sphinx documentation including API docs.'''
    #ctx.run("{0} -m sphinx.quickstart -p '{{parentcap}}{{joiner}}{{projectcap}}' -a '{{author}}' -v {{version}} --no-batchfile --no-makefile --ext-autodoc --ext-viewcode -q docs".format(sys.executable), pty=True, shell='/bin/sh')
    ctx.run('{0} -m sphinx.apidoc -f -o docs/ {1}'.format(sys.executable,
        '/'.join(ctx.proj_name.split('.')[:-1])), pty=True, shell='/bin/sh')
    ctx.run('{0} setup.py build_sphinx {1}'.format(sys.executable, opts),
        pty=True, shell='/bin/sh')


try:
	from tasks_addcmds import *
except ImportError as exc:
	print(repr(exc))
