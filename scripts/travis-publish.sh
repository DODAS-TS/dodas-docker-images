#!/bin/bash

if [[ `git diff-tree --no-commit-id --name-only -r HEAD~2 | grep "$3"` ]]; then

    docker tag $1 $2
    docker push $2
    docker push $1

fi