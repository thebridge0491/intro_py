#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals)

import warnings, sys, os, inspect, fileinput, re
from future.builtins import *

__all__ = ['main']


warnings.simplefilter('module')

setX = 'problems_perl'

def xform_args(args, path_pfx):
    return map(lambda f: f if None == path_pfx else 
        "{0}/{1}/{2}".format(path_pfx, setX, f), args)

def _create_contents_generator(dirs):
    '''Create contents generator'''    
    
    for dir1 in dirs:
        for root, dirnames, filenames in os.walk(dir1):
            for file1 in filenames:
                yield os.path.join(root, file1)

def _create_files_dicts(dir1, dir2):
    '''Create dictionaries of all files(directories 1 & 2) for two 
    directories'''
    
    filesAR, filesA = {}, _create_contents_generator([dir1])
    filesBR, filesB = {}, _create_contents_generator([dir2])
    
    for file1 in filesA:
        filesAR[os.path.basename(file1)] = file1
        filesBR[os.path.basename(file1)] = None
    
    for file1 in filesB:
        filesBR[os.path.basename(file1)] = file1
        
        if not os.path.basename(file1) in filesAR:
            filesAR[os.path.basename(file1)] = None
    
    return (filesAR, filesBR)

def create_diff_generator(dirs, opt_differ=True, opt_same=True, opt_dir1=True,
        opt_dir2=True, path_pfx = os.environ.get('PATH_PFX')):
    '''Create diff generator'''
    import difflib
    
    (filesAR, filesBR) = _create_files_dicts(*xform_args(dirs, path_pfx))
    
    for tester in sorted(filesAR.keys()):
        coexist = filesAR[tester] and filesBR[tester]
        
        if opt_dir1 and not filesBR[tester]:
            yield '<<< {0}'.format(tester)
        if opt_dir2 and not filesAR[tester]:
            yield '>>> {0}'.format(tester)
        
        if coexist:
            fromfile, tofile = filesAR[tester], filesBR[tester]
            
            with open(fromfile, 'rt') as fileF, open(tofile, 'rt') as fileT:
                diff = difflib.context_diff(fileF.readlines(),
                    fileT.readlines(), fromfile, tofile)
            
            if opt_differ and list(diff):
                yield '< {0} >'.format(tester)
            elif opt_same and not list(diff):
                yield '> {0} <'.format(tester)

def main(argv = None):
    '''Main entry'''
    
    paths = filter(lambda e: not re.search('^-.*', str(e)), argv)
    opts = list(filter(lambda e: re.search('^-.*', str(e)), argv))
    opts_dict = {} if 0 == len(opts) else {
        'opt_differ': any(filter(lambda o: re.search('d', o), opts)),
        'opt_same': any(filter(lambda o: re.search('s', o), opts)),
        'opt_dir1': any(filter(lambda o: re.search('1', o), opts)),
        'opt_dir2': any(filter(lambda o: re.search('2', o), opts))}
    
    # Performs diff on similar named files in two cmdline arg directories and
    # indicates status if file names and/or contents do/don't match.
    #
    # Uses the following symbols around file names to indicate status:
    #   unmatched file in dir1      : <<< file1
    #   unmatched file in dir2      : >>> file2
    #   similar name but different  : < file >
    #   similar name and same       : > file <
    # demo: $ script [-ds12] <path>/dataA <path>/dataB
    for line in create_diff_generator(list(paths), **opts_dict):
        print(line)
    
    return 0


if '__main__' == __name__:
    raise SystemExit(main(sys.argv[1:]))
