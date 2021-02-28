# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import os, sys, pkgutil, json, glob
from distutils.command.clean import clean as CleanCommand
from setuptools import setup, find_packages, Command
from builtins import open, dict

PROJECT = 'intro_py.util'
HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.extend([os.path.join(HERE, '..')])

def disable_commands(*blacklist):
    bad_cmds = [arg for cmd in blacklist for arg in sys.argv if cmd in arg]
    if [] != bad_cmds:
        print('Command(s) {0} have been disabled; exiting'.format(bad_cmds))
        raise SystemExit(2)

disable_commands('register', 'upload')

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
        if 1 != self.all:
            return
        _remove_pathlist(_matches_filepatterns(['build', 'dist', '*.egg*',
            '.cache', '__pycache__', '.hypothesis', 'htmlcov', '.tox', '*.so',
            '*.pyc', '*.pyo', '*~', '.coverage*', '*.log', '*.class'], ['.']))

class Test0(Command):
    ## nose2 cmd description
    #description = 'run nose2 [DEBUG=1] (* addon *)'
    description = 'run unittest discover [DEBUG=1] (* addon *)'
    user_options = [('opts=', 'o', 'Test options (default: -s {0})'.format(
        '/'.join(PROJECT.split('.')[:-1])))]
    def initialize_options(self):
        self.cwd, self.opts = None, ''
    def finalize_options(self):
        self.cwd = os.getcwd()
    def run(self):
        import subprocess
        assert os.getcwd() == self.cwd, 'Must be in pkg root: {0}'.format(
            self.cwd)
        ## use nose2
        #errno = subprocess.call('{0} -m nose2 {1}'.format(
        #    sys.executable, self.opts), shell = True)
        errno = subprocess.call('{0} -m unittest discover {1}'.format(
            sys.executable, self.opts), shell = True)
        raise SystemExit(errno)

cmds_addon = {}

if '1' == os.environ.get('DEBUG', '0').lower():
    sys.executable = '{0} -m coverage run'.format(sys.executable)

# setuptools add-on cmds
try:
	import setup_addcmds
	cmds_addon.update(setup_addcmds.cmdclass)
except ImportError as exc:
	print(repr(exc))

with open('README.rst') as f_in:
    readme = f_in.read()

with open('HISTORY.rst') as f_in:
    history = f_in.read()

json_bytes = pkgutil.get_data(PROJECT, 'resources/pkginfo.json')
pkginfo = json.loads(json_bytes.decode(encoding='utf-8')) if json_bytes is not None else {}

licenseclassifiers = {
	"Apache-2.0": "License :: OSI Approved :: Apache Software License",
    "MIT": "License :: OSI Approved :: MIT License",
    "BSD-3-Clause": "License :: OSI Approved :: BSD License",
    "GPL-3.0+": "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "ISC": "License :: OSI Approved :: ISC License (ISCL)",
    "Unlicense": "License :: Public Domain"
}

setup(
    long_description=readme + '\n\n' + history,
    classifiers=[
        "Natural Language :: English",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        licenseclassifiers.get('Apache-2.0', "License :: OSI Approved :: Apache Software License"),
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: Jython",
        "Topic :: Software Development"
    ],
    #package_dir={'': '.'},
    #packages=find_packages(include=[PROJECT, '{0}.tests'.format(PROJECT.replace('.', '/'))]),
    packages=find_packages(),
    # py_modules=[splitext(basename(path))[0] for path in glob.glob('{0}/*.py'.format('/'.join(PROJECT.split('.')[:-1])))],
    #data_files=[('', ['{0}/tests/__main__.py'.format(PROJECT.replace('.', '/'))])], # DON'T USE
    #package_data={'': ['{0}/tests/__main__.py'.format(PROJECT.replace('.', '/'))]}, # DON'T USE
    #test_suite='{0}.tests'.format(PROJECT),
    
    cmdclass=dict(dict({'clean': Clean0, 'test': Test0}).items()
		# setuptools add-on cmds
		| cmds_addon.items()
        ),
    **pkginfo
)
