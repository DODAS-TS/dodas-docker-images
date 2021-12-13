# Image name: dodasts/cygno-lab
FROM dodasts/snj-base-lab-cc7

ARG JUPYTER_ROOT=/jupyter-workspace

COPY packages /tmp/

COPY post_script.sh /usr/local/share/dodasts/script/
RUN chmod +x /usr/local/share/dodasts/script/post_script.sh

# clean metadata: https://srvfail.com/yum-doesnt-work-in-clean-centos-7-install-exiting-on-user-cancel/
RUN yum -y clean metadata \
    && yum -y update \
    && yum -y upgrade \
    && xargs yum -y install < /tmp/packages \
    && yum -y clean all \
    && rm -f /tmp/packages

RUN jupyter labextension uninstall @jlab_collaborative_ext/context-menu

# Install Geant4
WORKDIR /tmp/
RUN wget --progress=bar http://cern.ch/geant4-data/releases/geant4.10.05.p01.tar.gz \
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
    && make install 
WORKDIR /tmp
RUN rm -rf geant4 geant4-build

# Install garfield
WORKDIR /usr/local/share/garfield
ENV GARFIELD_HOME=/usr/local/share/garfield
ENV HEED_DATABASE=${GARFIELD_HOME}/Heed/heed++/database
RUN git clone https://gitlab.cern.ch/garfield/garfieldpp.git ${GARFIELD_HOME} \
    && mkdir build
WORKDIR /usr/local/share/garfield/build
RUN cmake3 ${GARFIELD_HOME} \
    && make -j 4 \
    && make install 

WORKDIR /

# Install boto
RUN pip3 install --no-cache-dir -U git+https://github.com/DODAS-TS/boto3sts

# Install ca
RUN wget "https://crt.sh/?d=2475254782" --progress=bar -O /etc/pki/ca-trust/source/anchors/ca.crt \
    && update-ca-trust \
    && update-ca-trust force-enable

# Install 
RUN pip3 install --no-cache-dir -U mahotas \
    && pip3 install --no-cache-dir -U git+https://github.com/gmazzitelli/cygno_repo.git

# Link folders
RUN mkdir -p ${JUPYTER_ROOT} \
    && ln -s /s3 ${JUPYTER_ROOT}/cloud-storage \
    && ln -s /shared ${JUPYTER_ROOT}/shared \
    && ln -s /private ${JUPYTER_ROOT}/private

RUN alternatives --set python /usr/bin/python3


WORKDIR /jupyter-workspace