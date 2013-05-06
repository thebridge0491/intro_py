{{cookiecutter.parentcap}}
===========================================
.. .rst to .html: rst2html5 foo.rst > foo.html
..                pandoc -s -f rst -t html5 -o foo.html foo.rst

{{cookiecutter.parentdescription}}

Installation
------------
source code tarball download:
    
        # [aria2c --check-certificate=false | wget --no-check-certificate | curl -kOL]
        
        FETCHCMD='aria2c --check-certificate=false'
        
        $FETCHCMD https://{{cookiecutter.repohost}}/{{cookiecutter.repoacct}}/{{cookiecutter.parent}}/[get | archive]/master.zip

version control repository clone:
        
        git clone https://{{cookiecutter.repohost}}/{{cookiecutter.repoacct}}/{{cookiecutter.parent}}.git

Author/Copyright
----------------
Author: {{cookiecutter.author}} <{{cookiecutter.email}}>
    
see sub-package's Author/Copyright

License
-------
see sub-package's License
