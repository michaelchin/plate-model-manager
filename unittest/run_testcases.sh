#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
#echo "$BASEDIR"
cd $BASEDIR/testcases
python3 -m unittest 