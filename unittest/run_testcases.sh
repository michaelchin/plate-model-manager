#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
#echo "$BASEDIR"
cd $BASEDIR
#export TEST_LEVEL=1
python3 -m unittest -vv --buffer 