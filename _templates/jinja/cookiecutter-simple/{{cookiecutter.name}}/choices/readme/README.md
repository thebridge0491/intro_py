# {{cookiecutter.projectcap}}
<!-- .md to .html: markdown foo.md > foo.html
                   pandoc -s -f markdown_strict -t html5 -o foo.html foo.md -->

{{cookiecutter.description}}

## Installation
source code tarball download:
    
        # [aria2c --check-certificate=false | wget --no-check-certificate | curl -kOL]
        FETCHCMD='aria2c --check-certificate=false'
        $FETCHCMD https://{{cookiecutter.repohost}}/{{cookiecutter.repoacct}}/{{cookiecutter.project}}/[get | archive]/master.zip

version control repository clone:
        
        git clone https://{{cookiecutter.repohost}}/{{cookiecutter.repoacct}}/{{cookiecutter.project}}.git

## Usage
        TODO - fix usage info

## Author/Copyright
Copyright (c) {{cookiecutter.year}} by {{cookiecutter.author|default(cookiecutter.repoacct)}} <{{cookiecutter.email|default("{0}-codelab@yahoo.com".format(cookiecutter.repoacct))}}>
{% if 'Not open source' != cookiecutter.license %}

## License
Licensed under the {{cookiecutter.license}} License. See LICENSE for details.
{% endif %}