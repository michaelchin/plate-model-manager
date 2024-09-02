#!/bin/bash

if [ -z "$1" ]; then
    echo ERROR: missing version number
    echo usage: create_tag.sh 1.3.0
    exit 1
fi

BASEDIR=$(dirname "$0")
cd "$BASEDIR"/..

# create and push a new tag
# a github workflow will pick up the new tag and create a new release automatically
git tag v$1
git push origin v$1