#!/usr/bin/env bash

mkdir -p /usr/local/share/CYGNO-MC

pushd /usr/local/share/CYGNO-MC || exit 1

git clone --branch lime https://github.com/CYGNUS-RD/CYGNO-MC . &&
    mkdir -p /usr/local/share/CYGNO-MC/CYGNO-MC-build

pushd /usr/local/share/CYGNO-MC/CYGNO-MC-build || exit 2

source /usr/local/share/geant4/bin/geant4.sh

cmake3 -Dcadmesh_DIR=/usr/local/share/CADMesh/ \
    -Werror=dev .. || exit 3
make -j 8

popd || exit 4
popd || exit 5

