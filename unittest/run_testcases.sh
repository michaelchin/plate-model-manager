#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
#echo "$BASEDIR"
cd $BASEDIR
#export PMM_TEST_LEVEL=1
python3 -m unittest -vv --buffer 