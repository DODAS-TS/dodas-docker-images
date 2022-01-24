#!/usr/bin/env bash

git clone https://gitlab.cern.ch/garfield/garfieldpp.git "${GARFIELD_HOME}" && mkdir build

pushd /usr/local/share/garfield/build || exit 1

cmake3 "${GARFIELD_HOME}" &&
    make -j 4 &&
    make install

popd || exit 2
