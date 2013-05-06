#!/bin/sh

mkdir -p build ; cp -R choices build/
rm -r choices

cp build/choices/readme/README{{readmeext}} README{{readmeext}}
cp build/choices/_parent_readme/README{{readmeext}} build/choices/_parent_init/README{{readmeext}}

if ! [ 'Not open source' = '{{license}}' ] ; then
    cp build/choices/license/LICENSE_{{license}} LICENSE ;
fi

if ! [ 'setuptools' = '{{buildtool}}' ] ; then
	cp -R build/choices/build_tool/{{buildtool}}/* . ;
else # default: setuptools
	cp -R build/choices/build_tool/setuptools/* . ;
fi

if ! [ 'unittest' = '{{testfrwk}}' ] ; then
	cp -R build/choices/testfrwk/{{testfrwk}}/* {{nesteddirs}} ;
else # default: unittest
	cp -R build/choices/testfrwk/unittest/* {{nesteddirs}} ;
fi

if ! [ 'yes' = '{{executable}}' ] ; then
    rm {{nesteddirs}}/__main__.py {{nesteddirs}}/cli.py ;
fi

if [ '' = "$(echo '{{ffilib}}' | grep -E 'none')" ] ; then
	cp -R build/choices/ffi_lib/{{ffilib}}/* {{nesteddirs}} ;
fi

# python -m sphinx.quickstart -p '{{parentcap}}{{joiner}}{{projectcap}}' -a '{{author}}' -v {{version}} --no-batchfile --no-makefile --ext-autodoc --ext-viewcode -q docs
#python -m sphinx.apidoc -o docs/ `dirname {{namespace}}`

if [ -d '../_templates' ] ; then
	mkdir -p ../_templates/jinja2 ;
	skel_pardir=`dirname {{_template}}` ;
	cp -R {{_template}} $skel_pardir/render_jinja2.* ../_templates/jinja2/ ;
fi
