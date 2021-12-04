#!/bin/sh

PROJECT_REGEX='{{cookiecutter.projectregex}}'
project_name='{{cookiecutter.project}}'

if [ "" = "$(echo $project_name | grep -E $PROJECT_REGEX)" ] ; then
    printf 'ERROR: The package (%s) is not a valid Python project name. Please do not use a - and use _ instead\n' "$project_name" ;
    
    #Exit to cancel project generation
    exit 1;
fi
