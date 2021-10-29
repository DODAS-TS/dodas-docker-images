# Image name: dodasts/cygno-lab
FROM dodasts/snj-base-lab-cc7

COPY packages packages

RUN yum update -y \
    && yum upgrade -y \
    && yum install -y epel-release \
    && yum install -y $(cat packages) \
    && yum clean all \
    && rm -f packages

# Install Geant4
WORKDIR /tmp/
RUN wget http://cern.ch/geant4-data/releases/geant4.10.05.p01.tar.gz \
    && tar -xzf "geant4.10.05.p01.tar.gz" \
    && mv "geant4.10.05.p01" geant4 \
    && rm "geant4.10.05.p01.tar.gz" 

WORKDIR /tmp/geant4-build
RUN cmake3 -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr/local/geant4 \
    -DGEANT4_INSTALL_DATA=ON \
    -DGEANT4_USE_SYSTEM_CLHEP=OFF \
    -DGEANT4_USE_SYSTEM_EXPAT=OFF \
    -DGEANT4_USE_GDML=ON \
    -DGEANT4_USE_OPENGL_X11=ON \
    -DGEANT4_USE_QT=ON \
    -DGEANT4_USE_XM=ON \
    -DGEANT4_BUILD_MULTITHREADED=ON \
    ../geant4 \ 
    && make -j4 \
    && make install \
    && cd ..\
    && rm -rf geant4 geant4-build

# Install garfield
WORKDIR /usr/local/share/garfield
ENV GARFIELD_HOME=/usr/local/share/garfield
ENV HEED_DATABASE=${GARFIELD_HOME}/Heed/heed++/database
RUN git clone https://gitlab.cern.ch/garfield/garfieldpp.git ${GARFIELD_HOME} \
    && mkdir build \
    && cd build \
    && cmake3 ${GARFIELD_HOME} \
    && make -j 4 \
    && make install 

WORKDIR /jupyter-workspace