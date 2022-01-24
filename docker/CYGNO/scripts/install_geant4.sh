#!/usr/bin/env bash

wget --progress=bar http://cern.ch/geant4-data/releases/geant4.10.05.p01.tar.gz &&
    tar -xzf "geant4.10.05.p01.tar.gz" &&
    mv "geant4.10.05.p01" geant4 &&
    rm "geant4.10.05.p01.tar.gz"

pushd /geant4-build || exit 1

cmake3 -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr/local/share/geant4 \
    -DGEANT4_INSTALL_DATA=ON \
    -DGEANT4_USE_SYSTEM_CLHEP=OFF \
    -DGEANT4_USE_SYSTEM_EXPAT=OFF \
    -DGEANT4_USE_GDML=ON \
    -DGEANT4_USE_OPENGL_X11=ON \
    -DGEANT4_USE_QT=ON \
    -DGEANT4_USE_XM=ON \
    -DGEANT4_BUILD_MULTITHREADED=ON \
    ../geant4 && make -j4 && make install

popd || exit 2

rm -rf geant4 geant4-build
