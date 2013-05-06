.POSIX:
.SUFFIXES:
PREFIX = /usr/local

DEBUG = 0

# Single package Makefile script.
#.SUFFIXES: .s .o .a .h .c
help:

# [python[2|3]|jython]
PYTHON = python
#PYTHONUSERBASE = $(PREFIX)/lib/python2.7/site-packages

pkg = {{cookiecutter.project}}
parent = {{cookiecutter.parent}}
proj = $(parent).$(pkg)
namespace_path = $(shell echo $(proj) | sed 'y|.|/|')
#version = $(shell sed -n 's|^Version: \(.*\)|\1|p' $(proj).*-info/* | uniq)
version = $(shell $(PYTHON) setup.py --version)
ver_major = $(shell echo $(version) | cut -d'.' -f1)

.PHONY: help build clean test develop install bdist_wheel sdist build_sphinx
help: ## help
	@echo "##### subproject: $(proj) #####"
	@echo "Usage: $(MAKE) [PYTHON=$(PYTHON)] [target] -- some valid targets:"
	$(PYTHON) setup.py --help-commands
build: ## build package [DEBUG=1] [ARGS=""]
	$(PYTHON) setup.py $@ $(ARGS)
clean: ## clean build artifacts [ARGS=""]
	$(PYTHON) setup.py $@ $(ARGS)
test: ## run tests [DEBUG=1] [TOPTS=""]
#	export [DY]LD_LIBRARY_PATH=. # ([da|ba|z]sh Linux)
#	setenv [DY]LD_LIBRARY_PATH . # (tcsh FreeBSD)
	-LD_LIBRARY_PATH=$(LD_LIBRARY_PATH):build/lib $(PYTHON) setup.py $@ $(TOPTS)
develop: ## to user's Python site-packages, python setup.py develop [ARGS=""]
	$(PYTHON) setup.py $@ $(ARGS)
install: ## to Python's site-packages, python setup.py install [ARGS=""]
	$(PYTHON) setup.py $@ $(ARGS)

bdist_wheel: ## create wheel distribution [ARGS=""]
	$(PYTHON) setup.py $@ $(ARGS)
sdist: ## create source distribution [ARGS=""]
	$(PYTHON) setup.py $@ $(ARGS)
build_sphinx: ## generate documentation [ARGS=""] (Sphinx HTML w/ API docs)
	$(PYTHON) setup.py $@ $(ARGS)

-include Makefile-addcmds.mk
#-include Makefile-auxffi.mk
