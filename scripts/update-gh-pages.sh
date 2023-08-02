#!/bin/bash

# this script is used in .github/workflows/build.yml
# it assumes the main branch is in folder "main"
# the gh-pages branch is in folder "gh-pages"

cp -rf ./main/doc/build/html/* ./gh-pages/

cd ./gh-pages/

git config --global user.name "michaelchin"
git config --global user.email "michael.chin@sydney.edu.au"

git add -A
git commit --message "GitHub Action to update github pages"
git push origin