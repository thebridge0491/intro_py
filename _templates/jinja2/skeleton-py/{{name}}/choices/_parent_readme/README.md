# {{parentcap}}
<!-- .md to .html: markdown foo.md > foo.html
                   pandoc -s -f markdown_strict -t html5 -o foo.html foo.md -->

{{parentdescription}}

## Installation
source code tarball download:
    
        # [aria2c --check-certificate=false | wget --no-check-certificate | curl -kOL]
        FETCHCMD='aria2c --check-certificate=false'
        $FETCHCMD https://{{repohost}}/{{repoacct}}/{{parent}}/[get | archive]/master.zip

version control repository clone:
        
        git clone https://{{repohost}}/{{repoacct}}/{{parent}}.git

## Author/Copyright
Author: {{author}} <{{email}}>

see sub-package's Author/Copyright

## License
see sub-package's License
