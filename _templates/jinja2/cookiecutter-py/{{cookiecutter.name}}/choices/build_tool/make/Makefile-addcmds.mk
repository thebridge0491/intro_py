# Targets Makefile script.
#----------------------------------------
# Common automatic variables legend (GNU make: make (Linux) gmake (FreeBSD)):
# $* - basename (cur target)  $^ - name(s) (all depns)  $< - name (1st depn)
# $@ - name (cur target)      $% - archive member name  $? - changed depns

ZIPOPTS := $(ZIPOPTS) -9 -q --exclude @$PWD/exclude.lst

.PHONY: pychecker pylint flake8 pep8 pep257 report html xml bdist_jar copyreqs zipreqs

pychecker: ## check style [ARGS=""] with pychecker
	-$(PYTHON) -m pychecker.checker $(ARGS) `find $(parent) -name '*.py' -a ! -name '__main__.py'`
pylint: ## check style [ARGS=""] with pylint
	-$(PYTHON) -m $@ --rcfile setup.cfg $(ARGS) $(proj)
flake8 pep8 pep257: ## check style [ARGS=""] with [flake8 | pep8 | pep257]
	-$(PYTHON) -m $@ $(ARGS) `find $(parent) -name '*.py'`
report html xml: ## report code coverage [ARGS=""]
	-$(PYTHON) -m coverage combine ; $(PYTHON) -m coverage $@ $(ARGS)
	if [ "$@" = "html"] && [ -e "htmlcov/index.html" ] ; then \
		w3m -M htmlcov/index.html ; fi

bdist_jar: ## create jar distribution
	-echo Class-Path: . > build/manifest.mf
	-jar -cfme dist/$(proj)-$(version).jar build/manifest.mf \
		org.python.util.JarRunner $(proj).* ;
	-zip $(ZIPOPTS) -r dist/$(proj)-$(version).jar .
build/pylib copyreqs: ## copy requirements to build/pylib
	-$(PYTHON) -m pip install -I -t build/pylib/site-packages -r requirements.txt
	-$(PYTHON) -m pip install -U -I --no-deps -t build/pylib -r requirements-internal.txt
	-find build/pylib -type d -name '*-info' -delete
zipreqs: build/pylib ## zip requirements to [wheel|jar] distribution
	-for archive in `ls $PWD/dist/$(proj)*.whl $PWD/dist/$(proj)*.jar` ; do \
		(cd build/pylib ; zip $(ZIPOPTS) -r $$archive * ; \
		zip $(ZIPOPTS) -d $$archive site-packages/copyreg\*) ; \
		(cd $(namespace_path)/tests ; zip $(ZIPOPTS) -r $$archive __main__.py) ; \
	done
