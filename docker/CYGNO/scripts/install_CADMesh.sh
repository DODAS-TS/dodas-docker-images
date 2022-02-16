#!/usr/bin/env bash

mkdir -p /usr/local/share/CADMesh

pushd /usr/local/share/CADMesh || exit 1

git clone --branch v1.1 https://github.com/christopherpoole/CADMesh.git . &&
    git submodule update --init --recursive &&
    mkdir -p /usr/local/share/CADMesh/build

pushd /usr/local/share/CADMesh/build || exit 2

cmake3 -DGeant4_DIR=/usr/local/share/geant4/lib64/Geant4-10.5.1/ -Werror=dev .. || exit 3
make -j 8 && make install

popd || exit 4
popd || exit 5
