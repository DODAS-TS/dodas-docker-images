#!/bin/bash

echo "git diff-tree --no-commit-id --name-only -r HEAD~1 | grep $2"

git diff-tree --no-commit-id --name-only -r HEAD~1 | grep -c No $2 

if [ $? -eq 0 ]; then
    docker build -t $1 $2
fi