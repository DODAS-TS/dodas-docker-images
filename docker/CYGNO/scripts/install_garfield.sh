#!/usr/bin/env bash

mkdir -p "${GARFIELD_HOME}"

pushd "${GARFIELD_HOME}" || exit 1

git clone https://gitlab.cern.ch/garfield/garfieldpp.git "${GARFIELD_HOME}" &&
    mkdir build &&
    mkdir -p "${GARFIELD_HOME}/build"

pushd "${GARFIELD_HOME}/build" || exit 2

cmake3 "${GARFIELD_HOME}" &&
    make -j 4 &&
    make install

popd || exit 3
popd || exit 4
