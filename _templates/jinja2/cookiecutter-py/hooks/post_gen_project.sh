#!/bin/sh

mkdir -p build ; cp -R choices build/
rm -r choices

cp build/choices/readme/README{{cookiecutter.readmeext}} README{{cookiecutter.readmeext}}
cp build/choices/_parent_readme/README{{cookiecutter.readmeext}} build/choices/_parent_init/README{{cookiecutter.readmeext}}

if ! [ 'Not open source' = '{{cookiecutter.license}}' ] ; then
    cp build/choices/license/LICENSE_{{cookiecutter.license}} LICENSE ;
fi

if ! [ 'setuptools' = '{{cookiecutter.buildtool}}' ] ; then
	cp -R build/choices/build_tool/{{cookiecutter.buildtool}}/* . ;
else # default: setuptools
	cp -R build/choices/build_tool/setuptools/* . ;
fi

if ! [ 'unittest' = '{{cookiecutter.testfrwk}}' ] ; then
	cp -R build/choices/testfrwk/{{cookiecutter.testfrwk}}/* {{cookiecutter.nesteddirs}} ;
else # default: unittest
	cp -R build/choices/testfrwk/unittest/* {{cookiecutter.nesteddirs}} ;
fi

if ! [ 'yes' = '{{cookiecutter.executable}}' ] ; then
    rm {{cookiecutter.nesteddirs}}/__main__.py {{cookiecutter.nesteddirs}}/cli.py ;
fi

if [ '' = "$(echo '{{cookiecutter.ffilib}}' | grep -E 'none')" ] ; then
	cp -R build/choices/ffi_lib/{{cookiecutter.ffilib}}/* {{cookiecutter.nesteddirs}} ;
fi

# python -m sphinx.quickstart -p '{{cookiecutter.parentcap}}{{cookiecutter.joiner}}{{cookiecutter.projectcap}}' -a '{{cookiecutter.author}}' -v {{cookiecutter.version}} --no-batchfile --no-makefile --ext-autodoc --ext-viewcode -q docs
#python -m sphinx.apidoc -o docs/ `dirname {{cookiecutter.namespace}}`

if [ -d '../_templates' ] ; then
	mkdir -p ../_templates/jinja2 ;
	cp -R {{cookiecutter._template}} ../_templates/jinja2/ ;
fi
