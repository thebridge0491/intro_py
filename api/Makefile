.POSIX:
.SUFFIXES:
PREFIX = /usr/local

DEBUG = 0

# Single package Makefile script.
help:

# [python[2|3]|jython]
PYTHON = python
#PYTHONUSERBASE = $(PREFIX)/lib/python3.8/site-packages

pkg = practice
parent = intro_py
proj = $(parent).$(pkg)
namespace_path = $(shell echo $(proj) | sed 'y|.|/|')
#version = $(shell sed -n 's|^Version: \(.*\)|\1|p' $(proj).*-info/* | uniq)
version = $(shell $(PYTHON) setup.py --version)
ver_major = $(shell echo $(version) | cut -d'.' -f1)

.PHONY: help build clean test develop install doc
help: ## help
	@echo "##### subproject: $(proj) #####"
	@echo "Usage: $(MAKE) [PYTHON=$(PYTHON)] [target] -- some valid targets:"
#	-@for fileX in $(MAKEFILE_LIST) `if [ -z "$(MAKEFILE_LIST)" ] ; then echo Makefile Makefile-addcmds.mk ; fi` ; do \
#		grep -ve '^[A-Z]' $$fileX | awk '/^[^.%][-A-Za-z0-9_]+[ ]*:.*$$/ { print "...", substr($$1, 1, length($$1)) }' | sort ; \
#	done
	-@for fileX in $(MAKEFILE_LIST) `if [ -z "$(MAKEFILE_LIST)" ] ; then echo Makefile Makefile-addcmds.mk ; fi` ; do \
		grep -E '^[ a-zA-Z_-]+:.*?## .*$$' $$fileX | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "%-25s%s\n", $$1, $$2}' ; \
	done
build: ##  build artifacts (create [source|wheel] distribution) [OPTS=""]
	$(PYTHON) -m build --no-isolation $(OPTS)
clean: ## clean build artifacts [OPTS=""]
	$(PYTHON) setup.py $@ $(OPTS)
test: ## run tests [DEBUG=1] [TOPTS=""]
#	export [DY]LD_LIBRARY_PATH=. # ([da|ba|z]sh Linux)
#	setenv [DY]LD_LIBRARY_PATH . # (tcsh FreeBSD)
	-LD_LIBRARY_PATH=$(LD_LIBRARY_PATH):build/lib $(PYTHON) -m unittest discover $(TOPTS)
develop: ## to user's Python site-packages, pip install --user [OPTS=""] -e .
#	$(PYTHON) setup.py develop $(OPTS)
	$(PYTHON) -m pip install --no-deps --no-build-isolation --user $(OPTS) -e .
	$(PYTHON) -m pip show $(proj)
install: ## to Python's site-packages, pip install --user [OPTS=""] .
	$(PYTHON) -m pip install --no-deps --no-build-isolation --user $(OPTS) .
	$(PYTHON) -m pip show $(proj)

doc: ## generate documentation [OPTS=""] (Sphinx HTML w/ API docs)
#	$(PYTHON) -m sphinx.cmd.quickstart -p Intro_py.Util -a  -v $(version) \
#		--no-batchfile --no-makefile --ext-autodoc --ext-viewcode -q docs
	$(PYTHON) -m sphinx.ext.apidoc -f -o docs/ $(parent)
	$(PYTHON) -m sphinx.cmd.build -b html $(OPTS) docs docs/_build

-include Makefile-addcmds.mk
#-include Makefile-auxffi.mk
