# Multi-package project Makefile script.
.POSIX:
help:

#MAKE = make # (GNU make variants: make (Linux) gmake (FreeBSD)
# [python[2|3]|jython]
PYTHON = python

parent = intro_py
SUBDIRS = common foreignc api app

.PHONY: build help clean test develop install
help: $(SUBDIRS)
	-for dirX in $^ ; do \
		(cd $$dirX ; $(PYTHON) setup.py --help-commands) ; done
	@echo "##### Top-level multiproject: $(parent) #####"
	@echo "Usage: $(MAKE) [SUBDIRS=$(SUBDIRS)] [PYTHON=$(PYTHON)] [target] --- some valid targets:"
build develop install: $(SUBDIRS)
	-for dirX in $^ ; do \
		(cd $$dirX ; $(PYTHON) setup.py $@ $(ARGS)) ; done
clean: $(SUBDIRS)
	-for dirX in $^ ; do \
		(cd $$dirX ; $(PYTHON) setup.py $@ $(ARGS)) ; done
	-rm -fr core* *~ .*~ build/* *.log */*.log __pycache__ *.pyc *.class
test: $(SUBDIRS)
	-for dirX in $^ ; do \
		(cd $$dirX ; $(PYTHON) setup.py $@ $(TOPTS)) ; done

#----------------------------------------
FMTS ?= tar.gz
distdir = $(parent)-0.1.0

.PHONY: bdist_wheel sdist build_sphinx checker report bdist_jar copyreqs zipreqs
sdist: $(SUBDIRS)
	-@mkdir -p build/$(distdir) ; cp -f exclude.lst build/
#	#-zip -9 -q --exclude @exclude.lst -r - . | unzip -od build/$(distdir) -
	-tar --format=posix --dereference --exclude-from=exclude.lst -cf - . | tar -xpf - -C build/$(distdir)
	
	-@for fmt in `echo $(FMTS) | tr ',' ' '` ; do \
		case $$fmt in \
			zip) echo "### build/$(distdir).zip ###" ; \
				rm -f build/$(distdir).zip ; \
				(cd build ; zip -9 -q -r $(distdir).zip $(distdir)) ;; \
			*) tarext=`echo $$fmt | grep -e '^tar$$' -e '^tar.xz$$' -e '^tar.bz2$$' || echo tar.gz` ; \
				echo "### build/$(distdir).$$tarext ###" ; \
				rm -f build/$(distdir).$$tarext ; \
				(cd build ; tar --posix -L -caf $(distdir).$$tarext $(distdir)) ;; \
		esac \
	done
	-@rm -r build/$(distdir)
	-for dirX in $^ ; do \
		(cd $$dirX ; $(PYTHON) setup.py $@ $(ARGS)) ; done
bdist_wheel build_sphinx checker report bdist_jar copyreqs zipreqs: $(SUBDIRS)
	-for dirX in $^ ; do \
		(cd $$dirX ; $(PYTHON) setup.py $@ $(ARGS)) ; done
