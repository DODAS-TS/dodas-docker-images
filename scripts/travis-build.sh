#!/bin/bash

echo "git diff-tree --no-commit-id --name-only -r HEAD~1 | grep $2"

CH_FILES=`git diff-tree --no-commit-id --name-only -r HEAD~1 | grep $2`

docker build -t $1 $2
