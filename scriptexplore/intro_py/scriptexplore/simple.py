#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals)

from functools import reduce
import warnings, sys, os, inspect, fileinput, re
#from builtins import *

__all__ = ['main']


warnings.simplefilter('module')

setX = 'simperl'

def xform_args(args, path_pfx):
    return map(lambda f: f if None == path_pfx else 
        "{0}/{1}/{2}".format(path_pfx, setX, f), args)

def simple01(args = "data01/file1 data01/file2 data01/file3 data01/file4 data01/file5".split(),
        path_pfx = os.environ.get('PATH_PFX')):
    '''problem 01: print cmd-line arguments 1 per line'''
    #<path>/maynard.pl 01 <path>/data01/arg[1 .. N]
    
    for arg in args:
        print(arg)

def simple02(args = "data02/file1 data02/file2 data02/file3 data02/file4 data02/file5".split(),
        path_pfx = os.environ.get('PATH_PFX')):
    '''problem 02: print all lines read with line number, space, line'''
    #<path>/maynard.pl 02 [<path>/data02/arg[1 .. N]]
    
    for line_num, line in enumerate(fileinput.input(xform_args(args, path_pfx))):
        print('{0} {1}'.format(line_num+1, line.rstrip('\r\n')))

def _create_logins_generator(args = None):
    '''Create logins generator'''
    
    for line in fileinput.input(args):
        fields = line.split(':')
        
        yield '{0:16}{1}'.format(fields[0], fields[4])

def simple03(args = "data03/file1 data03/file2".split(),
        path_pfx = os.environ.get('PATH_PFX')):
    '''problem 03: print logins and names (gcos field) of password-format file'''
    #<path>/maynard.pl 03 <path>/data03/arg[1 .. N]
    
    for line in _create_logins_generator(xform_args(args, path_pfx)):
        print(line)
    
def simple04(args = "data03/file1 data03/file2".split(),
        path_pfx = os.environ.get('PATH_PFX')):
    '''problem 04: print logins and names (gcos field) of password-format file sorted'''
    #<path>/maynard.pl 04 <path>/data03/arg[1 .. N]
    
    for line in sorted(_create_logins_generator(xform_args(args, path_pfx))):
        print(line)

def _create_contents_generator(is_dir = False, is_file = False, paths = None):
    '''Create contents generator, both dirs/files by default'''
    
    for dir1 in paths:
        for contents in os.listdir(dir1):
            path = os.path.join(dir1, contents.rstrip('\r\n'))
            is_valid_dir = (is_dir and os.path.isdir(path))
            
            if is_valid_dir or (is_file and os.path.isfile(path)):
                yield path

def simple05(args = "data05".split(),
        path_pfx = os.environ.get('PATH_PFX')):
    '''problem 05: print all file/directory names in directory from cmd-line'''
    #<path>/maynard.pl 05 <path>/data05
    
    for line in sorted(_create_contents_generator(is_dir = True, is_file = True,
            paths = xform_args(args, path_pfx))):
        print(line)
    
def simple06(args = "data05".split(),
        path_pfx = os.environ.get('PATH_PFX')):
    '''problem 06: print all regular file names in directory from cmd-line'''
    #<path>/maynard.pl 06 <path>/data05
    
    for line in sorted(_create_contents_generator(is_file = True, paths = xform_args(args, path_pfx))):
        print(line)
    
def simple07(args = "data05".split(),
        path_pfx = os.environ.get('PATH_PFX')):
    '''problem 07: print all directory names in directory from cmd-line'''
    #<path>/maynard.pl 07 <path>/data05
    
    for line in sorted(_create_contents_generator(is_dir = True, paths = xform_args(args, path_pfx))):
        print(line)

def _create_rename_generator(old, new, dirX):
    '''Create rename command generator'''
    
    extnew = '.{0}'.format(new)
    re_old = re.compile('\.{0}$'.format(old))
    
    for old_file in os.listdir(dirX):
        path = os.path.join(dirX, old_file.rstrip('\r\n'))
        
        if os.path.isfile(path):
            (new_file, num_replaced) = re_old.subn(extnew, path)
            if num_replaced:
                yield 'mv {0} {1}'.format(path, new_file)

def simple08(args = "for f data08".split(),
        path_pfx = os.environ.get('PATH_PFX')):
    '''problem 08: print mv cmds to chg file extension fm "for" to "f"'''
    #<path>/maynard.pl 08 for f <path>/data08
    
    usage_str = 'Usage: {0} 08 <old> <new> <dirX>\n'.format(sys.argv[0])
    
    if not 3 <= len(args):
        raise SystemExit(usage_str)
    (old, new, dir1toN) = (args[0], args[1], args[2:])
    
    for dirX in xform_args(dir1toN, path_pfx):
        for line in sorted(_create_rename_generator(old, new, dirX)):
            print(line)
    
def main(argv = None):
    '''Main entry'''
    
    switcher = {
        #None: simple01,
        '01': simple01,
        '02': simple02,
        '03': simple03,
        '04': simple04,
        '05': simple05,
        '06': simple06,
        '07': simple07,
        '08': simple08
    }
    usage_str = '  Usage: {0} simple<n> <arg1> [arg2 ..]\n\n  Available functions: {1}'.format(
        sys.argv[0], reduce(lambda a, k: (a + '\n    {}: '.format(k)) + 
        inspect.getdoc(switcher[k]), sorted(switcher.keys()), ""))
    
    #if not argv:
    #    raise SystemExit(usage_str)
    
    func = switcher.get(argv[0] if None != argv else '01', lambda *args:
        print('Invalid function: {0}\n{1}'.format(argv[0], usage_str)))
    func(argv[1:]) if None != argv and [] != argv[1:] else func()
    
    return 0


if '__main__' == __name__:
    raise SystemExit(main(sys.argv[1:]))
