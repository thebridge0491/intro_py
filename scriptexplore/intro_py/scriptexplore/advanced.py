#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, unicode_literals)

from functools import reduce
import warnings, sys, os, inspect, fileinput, re, glob
from future.builtins import *

__all__ = ['main']


warnings.simplefilter('module')

setX = 'perl'

def xform_args(args, path_pfx):
    return map(lambda f: f if None == path_pfx else 
        "{0}/{1}/{2}".format(path_pfx, setX, f), args)

def _create_mixed_generator(file1, file2):
    '''Create interleaved line generator'''    
    
    try:
        with open(file1, 'rt') as fhdl_1, open(file2, 'rt') as fhdl_2:
            while True:
                line1, line2 = fhdl_1.readline(), fhdl_2.readline()
                
                if line1:
                    yield line1.rstrip('\r\n')
                if line2:
                    yield line2.rstrip('\r\n')
                if not (line1 or line2):
                    break
    except IOError as ex:
        print(ex)

def advanced01(args = "data01/filea data01/fileb".split(),
        path_pfx = os.environ.get('PATH_PFX')):
    '''problem 01: interleave the lines of two files'''
    #<path>/maynard.pl 01 <path>/data01/arg[1 .. 2]
    
    for line in _create_mixed_generator(*xform_args(args, path_pfx)):
        print(line)

def _create_matching_line_generator(regexp, paths):
    '''Create matching line generator'''    
    
    rexp, files = re.compile(regexp), []
    
    for path in paths:
        if os.path.isfile(path):
            files.append(path)
        elif os.path.isdir(path):
            for file1 in os.listdir(path):
                cur_file = os.path.join(path, file1.rstrip('\r\n'))
                
                if os.path.isfile(cur_file):
                    files.append(cur_file)
    try:
        for line in fileinput.input(files):
            if rexp.search(line):
                line = line.rstrip('\r\n')
                yield '{0}:{1}'.format(fileinput.filename(), line)
    except UnicodeDecodeError as exc:
        #print(repr(exc), file=sys.stderr)
        pass

def advanced02(args = "ba+d data02/filea data02/fileb data02/dir/filec".split(),
        path_pfx = os.environ.get('PATH_PFX')):
    '''problem 02: grep for regexp in list of files fm cmd-line'''
    #<path>/maynard.pl 02 'ba+d' <path>/data02/arg[1 .. N]
    
    for line in _create_matching_line_generator(regexp = args[0], 
            paths = xform_args(args[1:], path_pfx)):
        print(line)

def _create_concat_generator(files):
    '''Create concatenated file(s) generator'''    
    
    for line in fileinput.input(files):
        yield line.rstrip('\r\n')

def advanced03(args = "data03/files1a data03/files2a data03/files3a".split(),
        path_pfx = os.environ.get('PATH_PFX')):
    '''problem 03: concatenate all files whose names given in files fm cmd-line'''
    #<path>/maynard.pl 03 <path>/data03/arg[1 .. N]
    
    paths = [path.rstrip('\r\n') for path in fileinput.input(xform_args(args, path_pfx))]
    for line in _create_concat_generator(xform_args(paths, path_pfx)):
        print(line)

def _create_remove_generator(search_name, paths,
        path_pfx = os.environ.get('PATH_PFX')):
    '''Create remove command generator for files matching search name in 
    paths'''
    
    import fnmatch  
    
    dirs = []
    
    for path in paths:
        if os.path.isdir(path):
            dirs.append(path)
        if os.path.isfile(path):
            for line in fileinput.input(path):
                dirs.append(list(xform_args([line.rstrip('\r\n')], path_pfx))[0])
    for dir1 in dirs:
        for root, dirnames, filenames in os.walk(dir1):
            for filename in fnmatch.filter(filenames, search_name):
                yield os.path.join(root, filename)
    
def advanced04(args = "data04/a data04/b data04/a/d".split(),
        path_pfx = os.environ.get('PATH_PFX')):
    '''problem 04: locate all core files in directories fm cmd-line'''
    #<path>/maynard.pl 04 <path>/data04/{a,b,a/d}
    
    for line in _create_remove_generator(search_name = 'core', paths = xform_args(args, path_pfx)):
        print("rm " + line)

def advanced05(args = "data05/dirsa".split(),
        path_pfx = os.environ.get('PATH_PFX')):
    '''problem 05: locate all core files in directories fm file fm cmd-line'''
    #<path>/maynard.pl 05 <path>/data05/dirs
    
    for line in _create_remove_generator(search_name = 'core', paths = xform_args(args, path_pfx)):
        print("rm " + line)
    
def advanced06(args = "ba+d data06".split(),
        path_pfx = os.environ.get('PATH_PFX')):
    '''problem 06: grep f/all occur's of regexp fm cmd-line in all text files'''
    #<path>/maynard.pl 06 'ba+d' <path>/data06
    
    for line in sorted(_create_matching_line_generator(regexp = args[0], 
            paths = xform_args(args[1:], path_pfx))):
        print(line)

def _create_rename_generator(new_base, files):
    '''Create rename command generator'''    
    
    for file1 in files:
        (fn_root, fn_ext) = os.path.splitext(file1)
        fn_dir, fn_base = os.path.dirname(file1), os.path.basename(file1)
        print(file1, file=sys.stderr)
        if not os.path.isfile(file1):
            continue
        
        new_file = os.path.join(fn_dir, '{0}{1}'.format(new_base, fn_ext))
        yield 'mv {0} {1}'.format(file1, new_file)
    
def advanced07(args = "solar data07/data.*".split(),
        path_pfx = os.environ.get('PATH_PFX')):
    '''problem 07: print mv cmds to chg basename for a set of files fm cmd-line'''
    #<path>/maynard.pl 07 solar <path>/data07/data.*
    
    for line in _create_rename_generator(new_base = args[0], 
			files = reduce(lambda a, p: a + glob.glob(p), 
			xform_args(args[1:], path_pfx), [])):
        print(line)

def _create_spammers_generator(files):
    '''Create spammers generator'''    
    
    for line in fileinput.input(files):
        match_1 = re.search('(\d+) .+ sendmail: \w+ (\S+).: user (.*)', line)
        match_2 = re.search(
                '(\d+) .+ sendmail: server (\S+@)?(\S+) (\S+) cmd (.*)', line)
        
        if match_1:
            yield '{0:40}    {1}'.format(match_1.groups()[1], 
                    match_1.groups()[0])
        elif match_2:
            yield '{0:40}    {1}'.format(match_2.groups()[2], 
                    match_2.groups()[0])

def advanced08(args = "data08".split(),
        path_pfx = os.environ.get('PATH_PFX')):
    '''problem 08: print cmds to list users of sendmail (possible spammers)'''
    #<path>/maynard.pl 08 <path>/data08
    
    for line in _create_spammers_generator(xform_args(args, path_pfx)):
        print(line)

def _bandwidth_usage_list(logfile):
    '''Compute bandwidth usage for input & output'''    
    
    usage_in, usage_out = ['Input', 0], ['Output', 0]
    
    for line in fileinput.input(logfile):
        match_use_in = re.search('Acct-Input-Packets = (\d+)', line)
        match_use_out = re.search('Acct-Output-Packets = (\d+)', line)
        
        if match_use_in:
            usage_in[1] += int(match_use_in.group(1))
        elif match_use_out:
            usage_out[1] += int(match_use_out.group(1))
    usage_list = []
    
    for txt, num in [usage_in, usage_out]:
        usage_list.append('Total {0} Bandwidth Usage = {1} packets'.format(
                txt, num))
        
    return usage_list

def _range_connects_list(logfile):
    '''Compute connections by ranges'''    
    
    rate144, rate192 = ['0-14400', 0], ['14401-19200', 0]
    rate288, rate336 = ['19201-28800', 0], ['28801-33600', 0]
    rateHi = ['above 33600', 0]
    
    for line in fileinput.input(logfile):
        match_rate = re.search('Ascend-Data-Rate = (\d+)', line)
        
        if match_rate:
            choice = int(match_rate.group(1))
            
            if 14400 >= choice:
                rate144[1] += 1
            elif 19200 >= choice:
                rate192[1] += 1
            elif 28800 >= choice:
                rate288[1] += 1
            elif 33600 >= choice:
                rate336[1] += 1
            else:
                rateHi[1] += 1
    connects_list = []
    
    for txt, num in [rate144, rate192, rate288, rate336, rateHi]:
        connects_list.append('{0:20}{1}'.format(txt, num))
        
    return connects_list

def _compute_minutes(logfile):
    '''Compute user minutes for events'''    
    
    time_totals = 0
    
    for line in fileinput.input(logfile):
        match_minutes = re.search('Acct-Session-Time = (\d+)', line)
        
        if match_minutes:
            time_totals += int(match_minutes.group(1))
    return ['Total User Session Time = {0}'.format(time_totals)]

def _usernames_generator(logfile, kwargs = None):
    '''Create user names generator'''    
    
    for line in fileinput.input(logfile):
        match_user = re.search('^\s+User-Name = "(.*)"$', line)
        
        if match_user:
            extra_quote = '' if kwargs['noquote'] else '"'
            yield '{0}{1}{0}'.format(extra_quote, match_user.group(1))

def _create_log_events_generator(logfile, kwargs = None):
    '''Create login/logout events generator'''    
    
    log_events_list = []
    
    if kwargs['user']:
        user_list = _usernames_generator(logfile = logfile, kwargs = kwargs)
        log_events_list.append(user_list)
    if kwargs['minutes']:
        minutes_computed = _compute_minutes(logfile = logfile,)
        log_events_list.append(minutes_computed)
    if kwargs['range_connects']:
        connects_list = _range_connects_list(logfile = logfile)
        log_events_list.append(connects_list)
    if kwargs['bandwidth']:
        bandwidth_list = _bandwidth_usage_list(logfile = logfile)
        log_events_list.append(bandwidth_list)
    
    return log_events_list
    
def advanced09(args = "data09".split(),
        path_pfx = os.environ.get('PATH_PFX')):
    '''problem 09: print user names in each event with quotes in ISP file'''
    #<path>/maynard.pl 09 <path>/data09 
    
    output_lists = _create_log_events_generator(logfile = xform_args(args, path_pfx), 
        kwargs = {'user': True, 'noquote': False, 'minutes': False, 
        'range_connects': False, 'bandwidth': False})
    
    for output_list in output_lists:
        for el in output_list:
            print(el)
        if 1 < len(output_lists):
            print('=' * 40)

def advanced10(args = "data10".split(),
        path_pfx = os.environ.get('PATH_PFX')):
    '''problem 10: print user names in each event without quotes in ISP file'''
    #<path>/maynard.pl 10 <path>/data10
    
    output_lists = _create_log_events_generator(logfile = xform_args(args, path_pfx), 
        kwargs = {'user': True, 'noquote': True, 'minutes': False, 
        'range_connects': False, 'bandwidth': False})
    
    for output_list in output_lists:
        for el in output_list:
            print(el)
        if 1 < len(output_lists):
            print('=' * 40)
        
def advanced11(args = "data11".split(),
        path_pfx = os.environ.get('PATH_PFX')):
    '''problem 11: compute total user minutes in ISP file'''
    #<path>/maynard.pl 11 <path>/data11
    
    output_lists = _create_log_events_generator(logfile = xform_args(args, path_pfx), 
        kwargs = {'user': False, 'noquote': True, 'minutes': True, 
        'range_connects': False, 'bandwidth': False})
    
    for output_list in output_lists:
        for el in output_list:
            print(el)
        if 1 < len(output_lists):
            print('=' * 40)
    
def advanced12(args = "data12".split(),
        path_pfx = os.environ.get('PATH_PFX')):
    '''problem 12: print number of connections with designated connect rates'''
    #<path>/maynard.pl 12 <path>/data12
    
    output_lists = _create_log_events_generator(logfile = xform_args(args, path_pfx), 
        kwargs = {'user': False, 'noquote': True, 'minutes': False, 
        'range_connects': True, 'bandwidth': False})
    
    for output_list in output_lists:
        for el in output_list:
            print(el)
        if 1 < len(output_lists):
            print('=' * 40)
    
def advanced13(args = "data13".split(),
        path_pfx = os.environ.get('PATH_PFX')):
    '''problem 13: print total input and output bandwidth usage in packets'''
    #<path>/maynard.pl 13 <path>/data13
    
    output_lists = _create_log_events_generator(logfile = xform_args(args, path_pfx), 
        kwargs = {'user': False, 'noquote': True, 'minutes': False, 
        'range_connects': False, 'bandwidth': True})
    
    for output_list in output_lists:
        for el in output_list:
            print(el)
        if 1 < len(output_lists):
            print('=' * 40)
    
def advanced14(args = "data14".split(),
        path_pfx = os.environ.get('PATH_PFX')):
    '''problem 14: print ???'''
    #<path>/maynard.pl 14 <path>/data14
    
def advanced15(args = "data15".split(),
        path_pfx = os.environ.get('PATH_PFX')):
    '''problem 15: ???'''
    #<path>/maynard.pl 15 <path>/data15
    
def main(argv = None):
    '''Main entry'''
    
    switcher = {
        #None: advanced01,
        '01': advanced01,
        '02': advanced02,
        '03': advanced03,
        '04': advanced04,
        '05': advanced05,
        '06': advanced06,
        '07': advanced07,
        '08': advanced08,
        '09': advanced09,
        '10': advanced10,
        '11': advanced11,
        '12': advanced12,
        '13': advanced13,
        '14': advanced14,
        '15': advanced15
    }
    usage_str = '  Usage: {0} advanced<n> <arg1> [arg2 ..]\n\n  Available functions: {1}'.format(
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
