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
	-for dirX in $^ ; do $(MAKE) -C $$dirX $@ ; done
	@echo "##### Top-level multiproject: $(parent) #####"
	@echo "Usage: $(MAKE) [SUBDIRS=$(SUBDIRS)] [PYTHON=$(PYTHON)] [target] --- some valid targets:"
build test develop install: $(SUBDIRS)
	-for dirX in $^ ; do $(MAKE) -C $$dirX $@ ; done
clean: $(SUBDIRS)
	-for dirX in $^ ; do $(MAKE) -C $$dirX $@ ; done
	-rm -fr core* *~ .*~ build/* *.log */*.log __pycache__ *.pyc *.class

#----------------------------------------
FMTS ?= tar.gz,zip
distdir = $(parent)-0.1.0

.PHONY: dist doc pylint flake8 pycodestyle pydocstyle pychecker report html xml bdist_jar copyreqs zipreqs
dist: $(SUBDIRS)
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
	-for dirX in $^ ; do $(MAKE) -C $$dirX build ; done
doc pylint flake8 pycodestyle pydocstyle pychecker report html xml bdist_jar copyreqs zipreqs: $(SUBDIRS)
	-for dirX in $^ ; do $(MAKE) -C $$dirX $@ ; done
