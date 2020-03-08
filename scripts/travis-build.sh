#!/bin/bash

echo "git diff-tree --no-commit-id --name-only -r HEAD~1 | grep $2"

CH_FILES=`git diff-tree --no-commit-id --name-only -r HEAD~1 | grep $2`

if ! docker pull $1; then
    docker build -t $1 $2
fi

