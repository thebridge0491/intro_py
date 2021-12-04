Intro_py.Foreignc
===========================================
.. .rst to .html: rst2html5 foo.rst > foo.html
..                pandoc -s -f rst -t html5 -o foo.html foo.rst

FFI sub-package for Python Intro examples project.

Installation
------------
source code tarball download:
    
        # [aria2c --check-certificate=false | wget --no-check-certificate | curl -kOL]
        
        FETCHCMD='aria2c --check-certificate=false'
        
        $FETCHCMD https://bitbucket.org/thebridge0491/intro_py/[get | archive]/master.zip

version control repository clone:
        
        git clone https://bitbucket.org/thebridge0491/intro_py.git

pip install --user -r <path>/requirements.txt

cd <path> ; pip install --user . --no-deps [--no-build-isolation]

python -m unittest discover

Usage
-----
        [env LD_LIBRARY_PATH=$PREFIX/lib] python -i intro_py/foreignc/classic.py
    
        >>> fact_i(5)

or
        [env LD_LIBRARY_PATH=$PREFIX/lib] python
        
        >>> from intro_py.foreignc import classic
        
        >>> classic.fact_i(5)

Author/Copyright
----------------
Copyright (c) 2013 by thebridge0491 <thebridge0491-codelab@yahoo.com>

License
-------
Licensed under the Apache-2.0 License. See LICENSE for details.
