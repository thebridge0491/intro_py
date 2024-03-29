# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import os, sys, pkgutil, json, glob
from distutils.command.clean import clean as CleanCommand
from setuptools import setup, find_packages, Command
#from setuptools import Extension # for Swig extension
from future.builtins import open, dict

PROJECT = '{{parent}}.{{project}}'
HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.extend([os.path.join(HERE, '..')])

## for cffi, swig
#if 'java' in sys.platform.lower():
#    raise Exception('This package can not be used with Jython.')

## for jna
#if 'java' not in sys.platform.lower():
#    raise Exception('This package can only be used with Jython.')
## jip install <groupId>:<artifactId>:<version> --> javalib/*.jar
## java -jar ivy.jar -dependency <groupId> <artifactId> '[<version>,)' -types jar -retrieve 'javalib/[artifact]-[revision](-[classifier]).[ext]'
#sys.path.extend(glob.glob('javalib/*.jar'))

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
{% if 'nose2' == testfrwk %}
    description = 'run nose2 [DEBUG=1] (* addon *)'
{% else %}
    description = 'run unittest discover [DEBUG=1] (* addon *)'
{% endif %}
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
{% if 'nose2' == testfrwk %}
        errno = subprocess.call('{0} -m nose2 {1}'.format(
            sys.executable, self.opts), shell = True)
{% else %}
        errno = subprocess.call('{0} -m unittest discover {1}'.format(
            sys.executable, self.opts), shell = True)
{% endif %}
        raise SystemExit(errno)

## for ffi_lib
#PREFIX = os.environ.get('PREFIX', '/usr/local')
#os.environ['LD_LIBRARY_PATH'] = ':'.join([
#    os.environ.get('LD_LIBRARY_PATH', '.'), '{}/lib'.format(PREFIX)])
#os.environ['LDFLAGS'] = ' '.join([
#    os.environ.get('LDFLAGS', '-Lbuild/lib'), '-L{}/lib'.format(PREFIX)])
#os.environ['CPPFLAGS'] = ' '.join([
#    os.environ.get('CPPFLAGS', '-Ibuild/include'),
#    '-I{}/include'.format(PREFIX)])

## for Swig extension
#extension_mod = Extension(name='{0}._classic_c'.format(PROJECT),
#    # sources=['{0}/classic_c_wrap.c'.format('build')],
#    sources=['{0}/classic_c.i'.format(PROJECT.replace('.', '/'))],
#    include_dirs=['.', PROJECT.replace('.', '/'), '{}/include'.format(PREFIX)],
#    library_dirs=os.environ.get('LD_LIBRARY_PATH', 'build/lib').split(':'),
#    libraries=[PROJECT],
#    runtime_library_dirs=['$ORIGIN/', '{}/lib'.format(PREFIX)],
#    extra_compile_args=os.environ.get('CPPFLAGS', '-Ibuild/include').split(' '),
#    extra_link_args=os.environ.get('LDFLAGS', '-Lbuild/lib').split(' '),
#    swig_opts=['-modern', '-I.']
#    )

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
        licenseclassifiers.get('{{license}}', "License :: OSI Approved :: Apache Software License"),
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
    ## for cffi
    #cffi_modules=['{0}/classic_build.py:ffibuilder'.format(
    #    PROJECT.replace('.', '/'))],
    ## for Swig extension
    #ext_modules=[extension_mod],
    cmdclass=dict(dict({'clean': Clean0, 'test': Test0}).items()
		# setuptools add-on cmds
		| cmds_addon.items()),
    **pkginfo
)
