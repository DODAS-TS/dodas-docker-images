#!/usr/bin/env bash

mkdir -p /usr/local/share/CADMesh

pushd /usr/local/share/CADMesh || exit 1

git clone --branch v1.1 https://github.com/christopherpoole/CADMesh.git . &&
    git submodule update --init --recursive &&
    mkdir -p /usr/local/share/CADMesh/build

pushd /usr/local/share/CADMesh/build || exit 2

RUN cmake3 .. &&
    make install

popd || exit 3
popd || exit 4
