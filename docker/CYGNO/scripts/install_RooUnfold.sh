#!/usr/bin/env bash

git clone --branch 2.0.1 https://gitlab.cern.ch/RooUnfold/RooUnfold.git . &&
    make &&
    make bin &&
    cp lib* /usr/lib64/root/ &&
    cp RooUnfoldDict_rdict.pcm /usr/lib64/root/
