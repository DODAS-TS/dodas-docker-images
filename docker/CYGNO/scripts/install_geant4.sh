#!/usr/bin/env bash

pushd /tmp || exit 1

wget --progress=bar http://cern.ch/geant4-data/releases/geant4.10.05.p01.tar.gz &&
    tar -xzf "geant4.10.05.p01.tar.gz" &&
    mv "geant4.10.05.p01" geant4 &&
    rm "geant4.10.05.p01.tar.gz" &&
    mkdir -p geant4-build

pushd geant4-build || exit 2

cmake3 -Werror=dev \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr/local/share/geant4 \
    -DGEANT4_INSTALL_DATA=ON \
    -DGEANT4_USE_SYSTEM_CLHEP=OFF \
    -DGEANT4_USE_SYSTEM_EXPAT=OFF \
    -DGEANT4_USE_GDML=ON \
    -DGEANT4_USE_OPENGL_X11=ON \
    -DGEANT4_USE_QT=ON \
    -DGEANT4_USE_XM=ON \
    -DGEANT4_BUILD_MULTITHREADED=ON \
    -DOpenGL_GL_PREFERENCE=GLVND \
    ../geant4 || exit 3

make -j 8 && make install

popd || exit 4

rm -rf geant4 geant4-build

popd || exit 5
