#!/usr/bin/env python
import os, glob, subprocess

def matches_filepatterns(filepats, paths):
	import fnmatch
	matches_pats = [os.path.join(root, file1) for path in paths
		for root, dirs, files in os.walk(path) for filepat in filepats
		for file1 in fnmatch.filter(dirs + files, filepat)]
	return matches_pats
	
def remove_pathlist(pathlist):
	import shutil
	for path in pathlist:
		if os.path.exists(path) and os.path.isdir(path):
			shutil.rmtree(path)
		elif os.path.exists(path):
			os.remove(path)
	
def copy_pathlist(pathlist, dst):
	import shutil
	for path in pathlist:
		if os.path.exists(path) and os.path.isdir(path):
			shutil.copytree(path, os.path.join(dst, os.path.basename(path)))
		elif os.path.exists(path) and not os.path.isdir(path):
			shutil.copy(path, dst)


if '__main__' == __name__:
	os.makedirs(os.path.join('build'), exist_ok=True)
	copy_pathlist(['choices'], 'build')
	remove_pathlist(['choices'])
	
	proj_dir = os.getcwd()
	choices = {
		'readmeext': '{{cookiecutter.readmeext|default('.rst')}}',
		'license': '{{cookiecutter.license|default('Apache-2.0')}}',
		'buildtool': '{{cookiecutter.buildtool|default('make')}}',
		'testfrwk': '{{cookiecutter.testfrwk|default('unittest')}}',
		'executable': '{{cookiecutter.executable|default('no')}}',
		'ffilib': '{{cookiecutter.ffilib|default('none')}}'
		}
	nesteddirs = '{{cookiecutter.nesteddirs|default('intro_py/util')}}'
	parent = '{{cookiecutter.parent|default('intro_py')}}'

	copy_pathlist(glob.glob('build/choices/readme/README{0}'.format(
		choices['readmeext'])), 'README{0}'.format(choices['readmeext']))
	if os.path.exists('build/choices/_parent_readme'):
		copy_pathlist(glob.glob('build/choices/_parent_readme/README{0}'.format(
			choices['readmeext'])), 'build/choices/_parent_init/README{0}'.format(
			choices['readmeext']))

	if choices['license'] in ['Apache-2.0', 'MIT', 'BSD-3-Clause', 'GPL-3.0+', 'ISC',
			'Unlicense']:
		copy_pathlist(glob.glob('build/choices/license/LICENSE_{0}'.format(
			choices['license'])), 'LICENSE')

	if os.path.exists('build/choices/build_tool') and choices['buildtool'] in [
			'make', 'invoke']:
		copy_pathlist(glob.glob('build/choices/build_tool/{0}/*'.format(
			choices['buildtool'])), '.')
	elif os.path.exists('build/choices/build_tool'): # default: make
		copy_pathlist(glob.glob('build/choices/build_tool/make/*'), '.')
	
	if os.path.exists('build/choices/testfrwk') and choices['testfrwk'] in ['unittest',
			'pytest', 'nose2']:
		copy_pathlist(glob.glob('build/choices/testfrwk/{0}/*'.format(
			choices['testfrwk'])), ".")
	elif os.path.exists('build/choices/testfrwk'): # default: unittest
		copy_pathlist(glob.glob('build/choices/testfrwk/unittest/*'),
			".")
	
	if os.path.exists("{0}".format(nesteddirs)) and 'yes' != choices['executable']:
		remove_pathlist(["{0}/__main__.py".format(nesteddirs),
			"{0}/cli.py".format(nesteddirs)])

	if os.path.exists('build/choices/ffi_lib') and choices['ffilib'] in ['ctypes',
			'cffi', 'swig', 'jna']:
		copy_pathlist(glob.glob('build/choices/ffi_lib/{0}/*'.format(
			choices['ffilib'])), "{0}/".format(nesteddirs))

	#quickstart.main("-- -p '{{cookiecutter.parentcap|default('Intro_py')}}{{cookiecutter.joiner|default('.')}}{{cookiecutter.projectcap|default('Util')}}' -a '{{cookiecutter.author|default(cookiecutter.repoacct)}}' -v {{cookiecutter.version}} --no-batchfile --no-makefile --ext-autodoc --ext-viewcode -q docs".split())
	#apidoc.main('-- -o docs/ {{(cookiecutter.parent|default('intro_py')).replace(".", "/")}}'.split())
	
	if os.path.exists('../_templates') and os.path.isdir('../_templates'):
		skeletondir = '{{cookiecutter._template}}'
		skel_pardir = os.path.dirname(skeletondir)
		remove_pathlist([os.path.join('../_templates/jinja/',
			os.path.basename(skeletondir))])
		os.makedirs(os.path.join('../_templates/jinja'), exist_ok=True)
		copy_pathlist(glob.glob('{0}/render_jinja.*'.format(
			skel_pardir))+[skeletondir], '../_templates/jinja/')
