# Targets Makefile script.
#----------------------------------------
# Common automatic variables legend (GNU make: make (Linux) gmake (FreeBSD)):
# $* - basename (cur target)  $^ - name(s) (all depns)  $< - name (1st depn)
# $@ - name (cur target)      $% - archive member name  $? - changed depns

ZIPOPTS := $(ZIPOPTS) -9 -q --exclude @${PWD}/exclude.lst

.PHONY: pylint flake8 pycodestyle pydocstyle pychecker report html xml bdist_jar copyreqs zipreqs

pylint: ## lint style [OPTS=""] with pylint
	-$(PYTHON) -m $@ $(OPTS) $(proj)
flake8 pycodestyle pydocstyle: ## lint style [OPTS=""] with [flake8 | pycodestyle | pydocstyle]
	-$(PYTHON) -m $@ $(OPTS) `find $(parent) -name '*.py'`
pychecker: ## lint style [OPTS=""] with pychecker
	-$(PYTHON) -m pychecker.checker $(OPTS) `find $(parent) -name '*.py' -a ! -name '__main__.py'`
report html xml: ## report code coverage [OPTS=""]
	-$(PYTHON) -m coverage combine ; $(PYTHON) -m coverage $@ $(OPTS)
	if [ "$@" = "html"] && [ -e "htmlcov/index.html" ] ; then \
		w3m -M htmlcov/index.html ; fi

bdist_jar: ## create jar distribution
	-echo Class-Path: . > build/manifest.mf
	-jar -cfme dist/$(proj)-$(version).jar build/manifest.mf \
		org.python.util.JarRunner $(proj).* ;
	-zip $(ZIPOPTS) -r dist/$(proj)-$(version).jar .
build/pylib copyreqs: ## copy requirements to build/pylib
	-$(PYTHON) -m pip install -U --no-deps --no-build-isolation -t build/pylib -r requirements-internal.txt
	-$(PYTHON) -m pip install -U -t build/pylib/site-packages -r requirements.txt
	-find build/pylib -type d -name '*-info' -exec rm -fr {} \;
zipreqs: build/pylib ## zip requirements to [wheel|jar] distribution
	-mkdir -p build/pylib
	-cp $(namespace_path)/tests/__main__.py build/pylib/
	-for archive in `pwd`/dist/$(proj)*.whl `pwd`/dist/$(proj)*.jar ; do \
		(cd build/pylib ; zip $(ZIPOPTS) -r $$archive *) ; \
	done
