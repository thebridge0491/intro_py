#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import os, sys, pkg_resources, setuptools, glob

pkg_resources.require('setuptools>=48.0')

HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.extend([HERE, os.path.join(HERE, '..')])

## for cffi, swig
#if 'java' in sys.platform.lower():
#    raise Exception('This package can not be used with Jython.')

## for jna
#if 'java' not in sys.platform.lower():
#    raise Exception('This package can only be used with Jython.')
## jip install <groupId>:<artifactId>:<version> --> javalib/*.jar
## java -jar ivy.jar -dependency <groupId> <artifactId> '[<version>,)' -types jar -retrieve 'javalib/[artifact]-[revision](-[classifier]).[ext]'
#sys.path.extend(glob.glob('javalib/*.jar'))

# for ffi_lib
PROJECT = 'intro_py.foreignc'
PREFIX = os.environ.get('PREFIX', '/usr/local')
os.environ['LD_LIBRARY_PATH'] = ':'.join([
    os.environ.get('LD_LIBRARY_PATH', '.'), '{}/lib'.format(PREFIX)])
os.environ['LDFLAGS'] = ' '.join([
    os.environ.get('LDFLAGS', '-Lbuild/lib'), '-L{}/lib'.format(PREFIX)])
os.environ['CPPFLAGS'] = ' '.join([
    os.environ.get('CPPFLAGS', '-Ibuild/include'),
    '-I{}/include'.format(PREFIX)])

## for Swig extension
#extension_mod = setuptools.Extension(name='{0}._classic_c'.format(PROJECT),
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


if __name__ == '__main__':
    # enable running setup.py from another directory
    HERE and os.chdir(HERE)
    
    # setuptools modified/add-on cmds
    cmds_addon = {}
    
    try:
        import setup_addcmds
        cmds_addon.update(setup_addcmds.cmdclass)
    except (ImportError, NameError) as exc:
        print(repr(exc))
    if '1' == os.environ.get('DEBUG', '0').lower():
        sys.executable = '{0} -m coverage run'.format(sys.executable)
    setuptools.setup(
        ## for cffi
        #cffi_modules=['{0}/classic_build.py:ffibuilder'.format(
        #    PROJECT.replace('.', '/'))],
        ## for Swig extension
        #ext_modules=[extension_mod],
    
        # setuptools modified/add-on cmds
        cmdclass=dict(dict({}) | cmds_addon.items())
    )
