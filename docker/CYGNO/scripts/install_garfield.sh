#!/usr/bin/env bash

mkdir -p "${GARFIELD_HOME}"

pushd "${GARFIELD_HOME}" || exit 1

git clone https://gitlab.cern.ch/garfield/garfieldpp.git "${GARFIELD_HOME}" &&
    mkdir build &&
    mkdir -p "${GARFIELD_HOME}/build"

pushd "${GARFIELD_HOME}/build" || exit 2

source /usr/local/share/geant4/bin/geant4.sh

cmake3 -Werror=dev "${GARFIELD_HOME}" || exit 3
make -j 8 && make install

popd || exit 4
popd || exit 5
