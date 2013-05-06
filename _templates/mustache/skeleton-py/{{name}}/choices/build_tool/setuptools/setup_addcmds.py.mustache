# -*- encoding: utf-8 -*-
from __future__ import absolute_import, print_function

from setuptools import Command
import os, subprocess, sys, glob, pkg_resources
from future.builtins import dict

__all__ = ['cmdclass']


os.environ['ZIPOPTS'] = '-9 -q --exclude @{0}/exclude.lst'.format(os.getcwd())
try:
    PROJECT = list(pkg_resources.find_distributions('.')
        )[0].project_name.replace('-', '_')
except IndexError as exc:
	print(repr(exc))

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

class Checker(Command):
    description = 'checker command(s) (default: pychecker) (* addon *)'
    user_options = [('opts=', 'o', 'Check options'), ('cmd=', 'c',
        'Checker cmd choices: [pychecker, pylint, flake8, pep8, pep257]')]
    def initialize_options(self):
        self.cwd, self.cmd, self.opts = None, 'pychecker', ''
    def finalize_options(self):
        self.cwd = os.getcwd()
    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in pkg root: {0}'.format(
            self.cwd)
        cmds_dict = {'pychecker': 'pychecker.checker',
            'pylint': 'pylint --rcfile setup.cfg', 'flake8': 'flake8',
            'pep8': 'pep8', 'pep257': 'pep257'}
        matches_wout_main = [file1 for file1 in _matches_filepatterns(
            ['*.py'], ['/'.join(PROJECT.split('.')[:-1]), 'tests']) if '__main__.py' not in file1]
        errno = subprocess.call('{0} -m {1} {2} {3}'.format(sys.executable,
            cmds_dict.get(self.cmd, 'pychecker.checker'),
            self.opts if self.opts else '', ' '.join(matches_wout_main)), 
            shell = True)
        raise SystemExit(errno)

class Report(Command):
    description = 'report code coverage (* addon *)'
    user_options = [('opts=', 'o', 'Report options'),
        ('type=', 't', 'PyCoverage report type: choices [report, html, xml]')]
    def initialize_options(self):
        self.cwd, self.type, self.opts = None, 'report', ''
    def finalize_options(self):
        self.cwd = os.getcwd()
    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in pkg root: {0}'.format(
            self.cwd)
        errno = subprocess.call('{0} -m coverage combine'.format(
            sys.executable), shell = True)
        errno = subprocess.call('{0} -m coverage {1} {2}'.format(
            sys.executable, self.type, self.opts if self.opts else ''),
            shell = True)
        if 'html' == self.type and os.path.exists('htmlcov/index.html'):
            errno = subprocess.call('w3m -M htmlcov/index.html', shell = True)
            #_browser_py('htmlcov/index.html')
        raise SystemExit(errno)

class BdistJar(Command):
    description = 'create a jar distribution (* addon *)'
    user_options = [('opts=', 'o', 'BdistJar options')]
    def initialize_options(self):
        self.cwd, self.opts = None, ''
    def finalize_options(self):
        self.cwd = os.getcwd()
    def run(self):
        VERSION = pkg_resources.get_distribution(PROJECT)._version
        assert os.getcwd() == self.cwd, 'Must be in pkg root: {0}'.format(
            self.cwd)
        errno = subprocess.call(
            'echo Class-Path: . > build/manifest.mf', shell = True)
        errno = subprocess.call(
            'jar -cfme dist/{0}-{1}.jar build/manifest.mf org.python.util.JarRunner {0}.*'.format(PROJECT, VERSION),
            shell = True)
        errno = subprocess.call(
            'zip {0} -r dist/{1}-{2}.jar .'.format(os.environ.get('ZIPOPTS', 
            ''), PROJECT, VERSION), shell = True)
        raise SystemExit(errno)

class CopyReqs(Command):
    description = 'copy requirements to build/pylib (* addon *)'
    user_options = [('opts=', 'o', 'CopyReqs options')]
    def initialize_options(self):
        self.cwd, self.opts = None, ''
    def finalize_options(self):
        self.cwd = os.getcwd()
    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in pkg root: {0}'.format(
            self.cwd)
        errno = subprocess.call(
            '{0} -m pip install -I -t build/pylib/site-packages -r requirements.txt'.format(sys.executable), shell = True)
        errno = subprocess.call(
            '{0} -m pip install -U -I --no-deps -t build/pylib -r requirements-internal.txt'.format(sys.executable), shell = True)
        _remove_pathlist(glob.glob('build/pylib/**/*-info'))
        raise SystemExit(errno)

class ZipReqs(Command):
    description = 'zip requirements to [wheel|jar] distribution (* addon *)'
    user_options = [('opts=', 'o', 'ZipReqs options')]
    def initialize_options(self):
        self.cwd, self.opts = None, ''
    def finalize_options(self):
        self.cwd = os.getcwd()
    def run(self):
        DISTROS = ' '.join(glob.glob('{0}/dist/{1}*.whl'.format(self.cwd, 
            PROJECT)) + glob.glob('{0}/dist/{1}*.jar'.format(self.cwd, 
            PROJECT)))
        assert os.getcwd() == self.cwd, 'Must be in pkg root: {0}'.format(
            self.cwd)
        errno = subprocess.call(
            'for archive in {3} ; do \
                cd {0}/build/pylib ; zip {2} -r $archive * ; \
                cd {0}/{1}/tests ; zip {2} -r $archive __main__.py ; \
            done'.format(self.cwd, PROJECT.replace('.', '/'),
            os.environ.get('ZIPOPTS', ''), DISTROS), shell = True)
        raise SystemExit(errno)

cmdclass = dict({'checker': Checker, 'report': Report,
    'bdist_jar': BdistJar, 'copyreqs': CopyReqs, 'zipreqs': ZipReqs
    })
