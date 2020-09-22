#!/bin/bash

NAME=${3/push\//}

echo "$NAME"

if [[ `git diff-tree --no-commit-id --name-only -r HEAD~2 | grep "$NAME"` ]]; then

    docker tag $1 $2
    docker push $2
    docker push $1

fi