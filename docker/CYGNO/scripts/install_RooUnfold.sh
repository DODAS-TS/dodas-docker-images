#!/usr/bin/env bash

mkdir -p /usr/local/share/RooUnfold

pushd /usr/local/share/RooUnfold || exit 1

git clone --branch 2.0.1 https://gitlab.cern.ch/RooUnfold/RooUnfold.git . &&
    make &&
    make bin &&
    cp lib* /usr/lib64/root/ &&
    cp RooUnfoldDict_rdict.pcm /usr/lib64/root/ || exit 2

popd || exit 3
