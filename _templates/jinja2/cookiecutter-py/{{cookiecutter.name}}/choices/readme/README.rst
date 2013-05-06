{{cookiecutter.parentcap}}{{cookiecutter.joiner}}{{cookiecutter.projectcap}}
===========================================
.. .rst to .html: rst2html5 foo.rst > foo.html
..                pandoc -s -f rst -t html5 -o foo.html foo.rst

{{cookiecutter.description}}

Installation
------------
source code tarball download:
    
        # [aria2c --check-certificate=false | wget --no-check-certificate | curl -kOL]
        
        FETCHCMD='aria2c --check-certificate=false'
        
        $FETCHCMD https://{{cookiecutter.repohost}}/{{cookiecutter.repoacct}}/{{cookiecutter.parent}}/[get | archive]/master.zip

version control repository clone:
        
        git clone https://{{cookiecutter.repohost}}/{{cookiecutter.repoacct}}/{{cookiecutter.parent}}.git

cd <path> ; pip install --user -e .

python setup.py test

Usage
-----
{% if 'yes' == cookiecutter.executable %}
        [env RSRC_PATH=<path>/resources] python -m {{cookiecutter.parent}}.{{cookiecutter.project}}

or
        [env RSRC_PATH=<path>/resources] python {{cookiecutter.nesteddirs}}/cli.py

or
        [env RSRC_PATH=<path>/resources] python
    
        >>> from {{cookiecutter.parent}}.{{cookiecutter.project}} import cli
    
        >>> cli.main([])
{% else %}
        python -i {{cookiecutter.nesteddirs}}/lib.py
    
        >>> cartesian_prod([0, 1, 2], [10, 20, 30])

or
        python
        
        >>> from {{cookiecutter.parent}} import {{cookiecutter.project}}
        
        >>> {{cookiecutter.project}}.cartesian_prod([0, 1, 2], [10, 20, 30])
{% endif %}

Author/Copyright
----------------
Copyright (c) {{cookiecutter.year}} by {{cookiecutter.author}} <{{cookiecutter.email}}>
{% if 'Not open source' != cookiecutter.license %}

License
-------
Licensed under the {{cookiecutter.license}} License. See LICENSE for details.
{% endif %}
