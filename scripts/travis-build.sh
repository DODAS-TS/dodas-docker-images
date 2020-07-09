#!/bin/bash

echo "git diff-tree --no-commit-id --name-only -r HEAD~1 | grep $2"

if [[ `git diff-tree --no-commit-id --name-only -r HEAD~1 | grep "$2"` ]]; then
    #docker pull $1
    docker build -t $1 $2
fi
