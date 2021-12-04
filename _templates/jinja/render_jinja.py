from __future__ import (absolute_import, division, print_function,
	unicode_literals)

import os, sys, glob, argparse, re, time
from future.builtins import (ascii, str, filter, hex, map, oct, zip)

from jinja2 import Environment, FileSystemLoader

SCRIPTPARENT = os.path.dirname(os.path.abspath(__file__))
CUR_DIR = os.path.abspath(os.curdir)

def deserialize_file(datapath, fmt='yaml', date_key='date'):
	initdata = {}
	
	if fmt in ['yaml', 'json']:
		try:
			import yaml						# [Base|Safe|Full]Loader
			with open(datapath) as fIn:
				initdata.update(yaml.load(fIn, Loader=yaml.SafeLoader))
		except ImportError as exc:
			print(repr(exc))
	elif 'toml' == fmt:
		try:
			import toml
			with open(datapath) as fIn:
				initdata.update(toml.load(fIn))
		except ImportError as exc:
			print(repr(exc))
	#elif 'json' == fmt:
	#	import json
	#	with open(datapath) as fIn:
	#		#initdata = json.load(fIn)
	#		initdata.update(json.load(fIn))
	
	initdata.update({date_key: time.strftime('%Y-%m-%d')})
	return initdata

def deserialize_str(datastr, fmt='yaml', date_key='date'):
	initdata = {}
	
	if datastr is not None:
		if fmt in ['yaml', 'json']:
			try:
				import yaml						# [Base|Safe|Full]Loader
				initdata.update(yaml.load(datastr, Loader=yaml.SafeLoader))
			except ImportError as exc:
				print(repr(exc))
		elif 'toml' == fmt:
			try:
				import toml
				initdata.update(toml.loads(datastr))
			except ImportError as exc:
				print(repr(exc))
		#elif 'json' == fmt:
		#	import json
		#	#initdata = json.loads(datastr.decode(encoding='utf-8'))
		#	initdata.update(json.loads(datastr))
	
	initdata.update({date_key: time.strftime('%Y-%m-%d')})
	return initdata

def regex_checks(pat, substr, txt):
	if not re.match(pat, substr):
		print("ERROR: Regex match failure (re.match({0}, {1})) for ({2}).".format(
			pat, substr, txt))
		sys.exit(1)

def derive_skel_vars(filebase, ctx=None):
	name = '{0}{1}{2}'.format(ctx.get('parent', ''), ctx.get('separator', ''),
		ctx['project'])
	parentcap = str.join(ctx.get('joiner', ''), map(lambda e: e.capitalize(),
		ctx.get('parent', '').split(ctx.get('separator', '-'))))
	namespace = '{0}{1}.{2}'.format(ctx['groupid'] + '.' if ctx.get('groupid')
		else '', ctx.get('parent', ''), ctx['project'])
	
	ctx.update({'year': ctx['date'].split('-')[0], 'name': name, 'parentcap': parentcap,
		'projectcap': ctx['project'].capitalize(), 'namespace': namespace,
		'nesteddirs': namespace.replace('.', '/')})
	return ctx if ctx.get('ignorefilebase', False) else {'filebase': filebase, filebase: ctx}

def render_skeleton(skeleton='skeleton-py', cfg=None):
	ctx = cfg[cfg['filebase']] if cfg.get('filebase') else cfg
	
	ctx.update({'_template': os.path.join(SCRIPTPARENT, skeleton)})
	start_dir = os.path.join(ctx['_template'], '{{{{{0}.name}}}}'.format(cfg.get('filebase')) if 
		cfg.get('filebase') else '{{name}}')
	files_skel = map(lambda p: os.path.relpath(p, start=start_dir), 
		filter(lambda p: os.path.isfile(p), glob.glob(start_dir + '/**/*',
		recursive=True)  + glob.glob(start_dir + '/**/.*', recursive=True)))
	renderouts, copyouts, pat_jinja = {}, {}, re.compile('\.jinja$')
	envPaths = Environment()
	for skelX in files_skel:
		template = envPaths.from_string(os.path.join(CUR_DIR, ctx['name'], skelX))
		if cfg.get('filebase'):
			renderouts[skelX] = template.render(cfg)
		else:
			if pat_jinja.search(skelX) :
				renderouts[skelX] = re.sub(pat_jinja, '', template.render(cfg))
			else:
				copyouts[skelX] = template.render(cfg)
	print('... processing files -- rendering {0} ; copying {1} ...'.format(
		len(renderouts), len(copyouts)))
	
	for dirX in [os.path.dirname(pathX) for pathX in 
			set(renderouts.values()) | set(copyouts.values())]:
		if not os.path.exists(os.path.join(CUR_DIR, ctx['name'], dirX)):
			os.makedirs(os.path.join(CUR_DIR, ctx['name'], dirX))
	envOuts = Environment(loader=FileSystemLoader(start_dir), trim_blocks=True)
	for srcR, dstR in renderouts.items():
		with open(os.path.join(CUR_DIR, ctx['name'], dstR), 'w+') as fOut:
			template = envOuts.get_template(srcR)
			fOut.write(template.render(cfg))
	for srcC, dstC in copyouts.items():
		with open(os.path.join(CUR_DIR, ctx['name'], dstC), 'w+') as fOut, \
				open(os.path.join(start_dir, srcC)) as fIn:
			fOut.write(fIn.read())
	
	print('Post rendering message')
	os.chdir(ctx['name'])
	os.system('python choices/post_gen_project.py') # python ___.py | sh ___.sh

def parse_cmdopts(args=None):
	opts_parser = argparse.ArgumentParser()
	
	opts_parser.add_argument('template', nargs='?', default='skeleton-py',
		help='Template path')
	opts_parser.add_argument('-d', '--data', default='data.yaml',
		help='Data path or - (for stdin)')
	opts_parser.add_argument('-f', '--datafmt', default='yaml',
		choices=[None, 'yaml', 'json', 'toml'], help='Specify data file format')
	#opts_parser.add_argument('-i', '--fileIn', type=argparse.FileType('r'),
	#	default=sys.stdin, help='File in - (for stdin) or path')
	opts_parser.add_argument('-o', '--fileOut', type=argparse.FileType('w'),
		default=sys.stdout, help='File out - (for stdout) or path')
	opts_parser.add_argument('-k', '--kvset', metavar='KEY=VALUE', nargs='+',
		help='Set key=value pairs (Ex: -k key1="val1")')
	
	return opts_parser.parse_args(args)

def main(argv=None):
	opts_hash, cfg = parse_cmdopts(argv), {}
	
	if not os.path.exists(opts_hash.template) and \
			not os.path.exists(os.path.join(SCRIPTPARENT, opts_hash.template)):
		print('Non-existent template: {0}'.format(opts_hash.template))
		sys.exit(1)
	kvset = dict(kv.split('=', 1) for kv in opts_hash.kvset) if opts_hash.kvset else None
	is_dir = os.path.isdir(opts_hash.template) or \
			os.path.isdir(os.path.join(SCRIPTPARENT, opts_hash.template))
	filebase_data = 'data' if '-' == opts_hash.data else \
		os.path.basename(opts_hash.data).split('.')[0]
	if '-' == opts_hash.data:
		cfg = deserialize_str(sys.stdin.read(), fmt=opts_hash.datafmt, date_key='date')
	
	if not is_dir:
		if not '-' == opts_hash.data:
			cfg = deserialize_file(opts_hash.data, fmt=opts_hash.datafmt, date_key='date')
		cfg.update(kvset if kvset else {})
	else:
		if not '-' == opts_hash.data:
			cfg = deserialize_file(os.path.join(SCRIPTPARENT, opts_hash.template,
				opts_hash.data), fmt=opts_hash.datafmt, date_key='date')
		cfg.update(kvset if kvset else {})
		cfg = derive_skel_vars(filebase_data, cfg)
		regex_checks(cfg.get('parentregex', ''), cfg.get('parent', ''), cfg.get('name', ''))
		regex_checks(cfg.get('projectregex', ''), cfg.get('project', ''), cfg.get('name', ''))
		
	switcher = {
		None: lambda: render_skeleton(opts_hash.template, cfg),
		True: lambda: render_skeleton(opts_hash.template, cfg),
		False: lambda: opts_hash.fileOut.write(Environment(
			loader=FileSystemLoader(CUR_DIR), trim_blocks=True).get_template(
			opts_hash.template).render(cfg))
	}
	func = switcher.get(is_dir, lambda:
		print('(is_dir: {0}) Invalid template: {1}'.format(is_dir, opts_hash.template)))
	return func()


if '__main__' == __name__:
	import sys
	#raise SystemExit(main(sys.argv[1:]))
	sys.exit(main(sys.argv[1:]))
