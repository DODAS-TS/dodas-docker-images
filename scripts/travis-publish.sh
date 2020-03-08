#!/bin/bash

docker tag $1 $2
docker push $2
docker push $1