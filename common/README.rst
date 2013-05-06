Intro_py.Util
===========================================
.. .rst to .html: rst2html5 foo.rst > foo.html
..                pandoc -s -f rst -t html5 -o foo.html foo.rst

Utilites sub-package for Python Intro examples project.

Installation
------------
source code tarball download:
    
        # [aria2c --check-certificate=false | wget --no-check-certificate | curl -kOL]
        
        FETCHCMD='aria2c --check-certificate=false'
        
        $FETCHCMD https://bitbucket.org/thebridge0491/intro_py/[get | archive]/master.zip

version control repository clone:
        
        git clone https://bitbucket.org/thebridge0491/intro_py.git

cd <path> ; pip install --user -e .

python setup.py test

Usage
-----
        python -i intro_py/util/lib.py
    
        >>> cartesian_prod([0, 1, 2], [10, 20, 30])

or
        python
        
        >>> from intro_py import util
        
        >>> util.cartesian_prod([0, 1, 2], [10, 20, 30])

Author/Copyright
----------------
Copyright (c) 2013 by thebridge0491 <thebridge0491-codelab@yahoo.com>

License
-------
Licensed under the Apache-2.0 License. See LICENSE for details.
