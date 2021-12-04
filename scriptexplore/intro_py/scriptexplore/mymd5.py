#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals)

import warnings, sys, os, inspect, fileinput, re
#from builtins import *

__all__ = ['main']


warnings.simplefilter('module')

setX = 'problems_perl'

def xform_args(args, path_pfx):
    return map(lambda f: f if None == path_pfx else 
        "{0}/{1}/{2}".format(path_pfx, setX, f), args)

def _create_contents_generator(pathX,
        path_pfx = os.environ.get('PATH_PFX')):
    '''Create contents generator'''    
    
    dirs = []
    
    for dir1 in fileinput.input(pathX):
        dirs.append(list(xform_args([dir1.rstrip('\r\n')], path_pfx))[0])
    dirs = sorted(dirs)
    
    for dir1 in dirs:
        for root, dirnames, filenames in os.walk(dir1):
            for path1 in filenames:
                yield os.path.join(root, path1)

def _compute_digest(filename=__file__, isSHA1=False):
    '''Compute hash digest (MD5 or SHA1) of file'''
    import hashlib
    
    hash_algo = hashlib.sha1() if isSHA1 else hashlib.md5()
    
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(128 * hash_algo.block_size), b''):
            hash_algo.update(chunk)
    return hash_algo.hexdigest()

def print_digest(rootpath, digestpath=None, isSHA1=False,
        path_pfx = os.environ.get('PATH_PFX')):
    '''Print hash digest to file'''    
    
    outfile = sys.stdout if None == digestpath else open(digestpath, 'wt')
    
    for path1 in _create_contents_generator(list(xform_args([rootpath], path_pfx))[0]):
        fingerprint = _compute_digest(path1, isSHA1)
        
        if not fingerprint:
            print('Error: hash digest on file {0}'.format(path1), 
                file=sys.stderr)
            continue
        outfile.write('{0}  {1}\n'.format(fingerprint, path1))
    outfile.close()

def _update_lines_dict(dict1, dict2, digestpath):
    '''Update two dictionaries of files -> digest'''

    for line in fileinput.input(digestpath):
        matches = re.search('^([^ \t]+)[ \t]*([^ \t]+)\n', line)
        
        if not matches:
            continue
        digest, file_name = matches.groups()
        
        if not file_name in dict2:
            dict2[file_name] = ''
        dict1[file_name] = digest
    
def verify_digest(rootpath, digestpath, isSHA1=False):
    '''Verifies hash digest of file(s)'''
    import tempfile
    
    cur_file = tempfile.NamedTemporaryFile(delete = False)
    cur_lines, digest_lines = {}, {}
    
    print_digest(rootpath, cur_file.name, isSHA1)
    
    _update_lines_dict(cur_lines, digest_lines, cur_file.name)
    _update_lines_dict(digest_lines, cur_lines, digestpath)
    
    for tester in sorted(digest_lines.keys()):
        if not (digest_lines[tester] and cur_lines[tester]):
            if digest_lines[tester]:
                print('<old>{0}  {1}'.format(tester, digest_lines[tester]))
            if cur_lines[tester]:
                print('<new>{0}  {1}'.format(tester, cur_lines[tester]))
        elif digest_lines[tester] != cur_lines[tester]:
            print('<old>{0}  {1}'.format(tester, digest_lines[tester]))
            print('<new>{0}  {1}'.format(tester, cur_lines[tester]))
            print('')
    
    os.unlink(cur_file.name)

def main(argv = None):
    '''Main entry'''
    
    paths = filter(lambda e: '-c' != e and '-s' != e, argv)
    
    if any(filter(lambda e: '-c' == e, argv)):
        # Verifies the hash digest (MD5 or SHA1) of all regular files under
        # any directories of command-line arg rootfile against the
        # command-line arg digestfile and indicates the status of changed,
        # added or deleted files in pairs
        #
        #Uses the following symbols to indicate status:
        #    <old>{file} {digest}        # for changed
        #    <new>{file} {digest}
        #    
        #    <new>{file} {digest}        # for added
        #    
        #    <old>{file} {digest}        # for deleted
        # demo: $ script [-s] -c <path>/rootfile.txt <path>/digestfile.txt
        verify_digest(*paths, isSHA1=any(filter(lambda e: '-s' == e, argv)))
    else:
        # Print the hash digest (MD5 or SHA1) of all regular files under any
        # directories of command-line arg file
        # demo: $ script [-s] <path>/rootfile.txt [<path>/digestfile.txt]
        print_digest(*paths, isSHA1=any(filter(lambda e: '-s' == e, argv)))
    
    return 0


if '__main__' == __name__:
    raise SystemExit(main(sys.argv[1:]))
