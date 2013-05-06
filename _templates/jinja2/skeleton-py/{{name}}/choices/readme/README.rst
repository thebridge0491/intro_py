{{parentcap}}{{joiner}}{{projectcap}}
===========================================
.. .rst to .html: rst2html5 foo.rst > foo.html
..                pandoc -s -f rst -t html5 -o foo.html foo.rst

{{description}}

Installation
------------
source code tarball download:
    
        # [aria2c --check-certificate=false | wget --no-check-certificate | curl -kOL]
        
        FETCHCMD='aria2c --check-certificate=false'
        
        $FETCHCMD https://{{repohost}}/{{repoacct}}/{{parent}}/[get | archive]/master.zip

version control repository clone:
        
        git clone https://{{repohost}}/{{repoacct}}/{{parent}}.git

cd <path> ; pip install --user -e .

python setup.py test

Usage
-----
{% if 'yes' == executable %}
        [env RSRC_PATH=<path>/resources] python -m {{parent}}.{{project}}

or
        [env RSRC_PATH=<path>/resources] python {{nesteddirs}}/cli.py

or
        [env RSRC_PATH=<path>/resources] python
    
        >>> from {{parent}}.{{project}} import cli
    
        >>> cli.main([])
{% else %}
        python -i {{nesteddirs}}/lib.py
    
        >>> cartesian_prod([0, 1, 2], [10, 20, 30])

or
        python
        
        >>> from {{parent}} import {{project}}
        
        >>> {{project}}.cartesian_prod([0, 1, 2], [10, 20, 30])
{% endif %}

Author/Copyright
----------------
Copyright (c) {{year}} by {{author}} <{{email}}>
{% if 'Not open source' != license %}

License
-------
Licensed under the {{license}} License. See LICENSE for details.
{% endif %}
