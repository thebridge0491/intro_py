# -*- encoding: utf-8 -*-
from __future__ import absolute_import, print_function

from setuptools import setup, find_packages, Command
from setuptools._distutils.command.clean import clean as CleanCommand
import os, subprocess, sys, glob, pkg_resources

__all__ = ['cmdclass']

os.environ['ZIPOPTS'] = '-9 -q --exclude @{0}/exclude.lst'.format(os.getcwd())
try:
    PROJECT = list(pkg_resources.find_distributions('.')
        )[0].project_name.replace('-', '_')
except IndexError as exc:
    PROJECT = 'UNKNOWN'
    print(repr(exc))

def disable_commands(*blacklist):
    bad_cmds = [arg for cmd in blacklist for arg in sys.argv if cmd in arg]
    if [] != bad_cmds:
        print('Command(s) {0} have been disabled; exiting'.format(bad_cmds))
        raise SystemExit(2)

disable_commands('register', 'upload')

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

class Clean0(CleanCommand):
    description = CleanCommand.description + ' (modified)'
    def run(self):
        import shutil
        CleanCommand.run(self)
        if not self.all:
            return
        _remove_pathlist(_matches_filepatterns(['build', 'dist', '*.egg*',
            '.cache', '__pycache__', '.hypothesis', 'htmlcov', '.tox', '*.so',
            '*.pyc', '*.pyo', '*~', '.coverage*', '*.log', '*.class'], ['.']))

class Test0(Command):
    description = 'test command(s) (default: unittest)) [DEBUG=1] (* addon *)'
    user_options = [('opts=', 'o', 'Test options (default: -s {0})'.format(
        '/'.join(PROJECT.split('.')[:-1]))), ('cmd=', 'c',
        'Test cmd choices: [unittest, nose2]')]
    def initialize_options(self):
        self.cwd, self.cmd = None, 'unittest'
        self.opts = '-s {0}'.format('/'.join(PROJECT.split('.')[:-1]))
    def finalize_options(self):
        self.cwd = os.getcwd()
    def run(self):
        import subprocess
        assert os.getcwd() == self.cwd, 'Must be in pkg root: {0}'.format(
            self.cwd)
        cmds_dict = {'unittest': 'unittest discover', 'nose2': 'nose2'}
        proc0 = subprocess.run('{0} -m {1} {2}'.format(sys.executable,
            cmds_dict.get(self.cmd, 'unittest'), self.opts), shell = True)
        print(proc0.args + '\n' if '-v' in self.opts else '', end='')
        raise SystemExit(proc0.returncode)

class Lint(Command):
    description = 'lint command(s) (default: pylint) (* addon *)'
    user_options = [('opts=', 'o', 'Lint options'), ('cmd=', 'c',
        'Lint cmd choices: [pylint, flake8, pydocstyle, pycodestyle, pychecker]')]
    def initialize_options(self):
        self.cwd, self.cmd, self.opts = None, 'pylint', ''
    def finalize_options(self):
        self.cwd = os.getcwd()
    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in pkg root: {0}'.format(
            self.cwd)
        cmds_dict = {'pycodestyle': 'pycodestyle', 'pydocstyle': 'pydocstyle',
            'pylint': 'pylint', 'flake8': 'flake8',
            'pychecker': 'pychecker.checker'}
        matches_wout_main = [file1 for file1 in _matches_filepatterns(
            ['*.py'], ['/'.join(PROJECT.split('.')[:-1]), 'tests']) if '__main__.py' not in file1]
        proc0 = subprocess.run('{0} -m {1} {2} {3}'.format(sys.executable,
            cmds_dict.get(self.cmd, 'pylint'), self.opts if self.opts else '',
            ' '.join(matches_wout_main)), shell = True)
        print(proc0.args + '\n' if '-v' in self.opts else '', end='')
        raise SystemExit(proc0.returncode)

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
        proc0 = subprocess.run('{0} -m coverage combine ; \
            {0} -m coverage {1} {2}'.format(sys.executable, self.type,
            self.opts if self.opts else ''), shell = True)
        print(proc0.args + '\n' if '-v' in self.opts else '', end='')
        if 'html' == self.type and os.path.exists('htmlcov/index.html'):
            proc0 = subprocess.run('w3m -M htmlcov/index.html', shell = True)
            print(proc0.args + '\n' if '-v' in self.opts else '', end='')
            #_browser_py('htmlcov/index.html')
        raise SystemExit(proc0.returncode)

class BdistJar(Command):
    description = 'create a jar distribution (* addon *)'
    user_options = [('opts=', 'o', 'BdistJar options')]
    def initialize_options(self):
        self.cwd, self.opts = None, ''
    def finalize_options(self):
        self.cwd = os.getcwd()
    def run(self):
        VERSION = '0.0.0'
        #VERSION = pkg_resources.get_distribution(PROJECT)._version
        try:
            if sys.version_info >= (3, 8):
                from importlib import metadata
            else:
                import importlib_metadata as metadata
            VERSION = metadata.version(PROJECT)
        except (ImportError, NameError) as exc:
            print(repr(exc))
        assert os.getcwd() == self.cwd, 'Must be in pkg root: {0}'.format(
            self.cwd)
        proc0 = subprocess.run(
            'echo Class-Path: . > build/manifest.mf ; \
            jar -cfme dist/{0}-{1}.jar build/manifest.mf org.python.util.JarRunner {0}.* ; \
            zip {2} -r dist/{0}-{1}.jar .'.format(PROJECT, VERSION,
            os.environ.get('ZIPOPTS', '')), shell = True)
        print(proc0.args + '\n' if '-v' in self.opts else '', end='')
        raise SystemExit(proc0.returncode)

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
        proc0 = subprocess.run(
            '{0} -m pip install -U --no-deps -t build/pylib -r requirements-internal.txt ; \
            {0} -m pip install -U -t build/pylib/site-packages -r requirements.txt'.format(sys.executable), shell = True)
        print(proc0.args + '\n' if '-v' in self.opts else '', end='')
        _remove_pathlist(glob.glob('build/pylib/**/*-info'))
        raise SystemExit(proc0.returncode)

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
        proc0 = subprocess.run(
            'mkdir -p {0}/build/pylib/ ; \
            cp {0}/{1}/tests/__main__.py {0}/build/pylib/ ; \
            for archive in {3} ; do \
                cd {0}/build/pylib ; zip {2} -r $archive * ; \
            done'.format(self.cwd, PROJECT.replace('.', '/'),
            os.environ.get('ZIPOPTS', ''), DISTROS), shell = True)
        print(proc0.args + '\n' if '-v' in self.opts else '', end='')
        raise SystemExit(proc0.returncode)

cmdclass = dict({'clean': Clean0, 'test': Test0, 'lint': Lint,
    'report': Report, 'copyreqs': CopyReqs, 'zipreqs': ZipReqs,
    'bdist_jar': BdistJar
    })
