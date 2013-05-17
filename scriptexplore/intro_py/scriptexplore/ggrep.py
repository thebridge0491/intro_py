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

def _create_files_list(paths):
    '''Create files list'''    
    
    dirs, files = [], []
    
    for path in paths:
        if os.path.isfile(path):
            files.append(path)
        elif os.path.isdir(path):
            dirs.append(path)
    files.extend(_create_contents_generator(dirs))
    return files

def create_grep_match_generator(regexp, paths, is_file_only=False,
        path_pfx = os.environ.get('PATH_PFX')):
    '''Create grep pattern match generator'''
    
    files = _create_files_list(xform_args(paths, path_pfx))
    
    try:
        for line in fileinput.input(files):
            if re.search(regexp, line):
                line = line.rstrip('\r\n')
                end_txt = '' if is_file_only else ':{0}'.format(line)
                
                yield fileinput.filename() + end_txt
                
                if is_file_only:
                    fileinput.nextfile()
    except UnicodeDecodeError as exc:
        #print(repr(exc)
        pass

def main(argv = None):
    '''Main entry'''
    
    params = filter(lambda e: '-l' != e, argv)
    
    # Greps for regular expression in all regular files in cmdline arg 
    # file/directory list as well as files under given directories
    # demo: $ script [-l] 'ba+d' <path>/filea <path>/fileb <path>/dir <path>/data6
    for line in create_grep_match_generator(next(params), list(params),
            is_file_only=any(filter(lambda e: '-l' == e, argv))):
        print(line)
    
    return 0


if '__main__' == __name__:
    raise SystemExit(main(sys.argv[1:]))
