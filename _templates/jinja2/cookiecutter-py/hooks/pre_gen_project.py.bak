import re
import sys

PROJECT_REGEX = r'{{cookiecutter.projectregex}}'
project_name = '{{cookiecutter.project}}'

if not re.match(PROJECT_REGEX, project_name):
    print('ERROR: package (%s) is not a valid Python module name. Please do not use a - and use _ instead' % project_name)

    #Exit to cancel project
    sys.exit(1)
