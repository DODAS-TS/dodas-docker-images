#!/usr/bin/env bash

git clone --branch v1.1 https://github.com/christopherpoole/CADMesh.git . &&
    git submodule update --init --recursive &&
    mkdir -p build

pushd /usr/local/share/CADMesh/build || exit 1

RUN cmake3 .. &&
    make install

popd || exit 2
