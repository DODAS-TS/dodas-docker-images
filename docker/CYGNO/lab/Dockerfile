# Image name: dodasts/cygno-lab
FROM dodasts/snj-base-lab-cc7:v1.0.0-snj

# Set python3 to default globally
# RUN update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1 \
#     && update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2 \
#     && yes 2 | update-alternatives --config python

ARG JUPYTER_ROOT=/jupyter-workspace

COPY assets/packages /tmp/

COPY scripts/install_geant4.sh /usr/local/share/dodasts/script/
RUN chmod +x /usr/local/share/dodasts/script/install_geant4.sh

COPY scripts/install_garfield.sh /usr/local/share/dodasts/script/
RUN chmod +x /usr/local/share/dodasts/script/install_garfield.sh

COPY scripts/install_CADMesh.sh /usr/local/share/dodasts/script/
RUN chmod +x /usr/local/share/dodasts/script/install_CADMesh.sh

COPY scripts/install_RooUnfold.sh /usr/local/share/dodasts/script/
RUN chmod +x /usr/local/share/dodasts/script/install_RooUnfold.sh

COPY scripts/post_script.sh /usr/local/share/dodasts/script/
RUN chmod +x /usr/local/share/dodasts/script/post_script.sh

# clean metadata: https://srvfail.com/yum-doesnt-work-in-clean-centos-7-install-exiting-on-user-cancel/
RUN yum -y clean metadata \
    && yum --exclude=\*oidc-agent\* -y update \
    && yum --exclude=\*oidc-agent\* -y upgrade \
    && xargs yum -y install < /tmp/packages \
    && yum -y clean all \
    && rm -f /tmp/packages

RUN jupyter labextension uninstall @jlab_collaborative_ext/context-menu

WORKDIR /usr/local/share/dodasts/script/

# garfield env variables
ENV GARFIELD_HOME=/usr/local/share/garfield
ENV HEED_DATABASE=${GARFIELD_HOME}/Heed/heed++/database

# Install Geant4
RUN ./install_geant4.sh
# Install garfield
RUN ./install_garfield.sh.sh
# Install CADMesh
RUN ./install_CADMesh.sh
# Install RooUnfold
RUN ./install_RooUnfold.sh

WORKDIR /

# Install boto
RUN pip3 install --no-cache-dir -U git+https://github.com/DODAS-TS/boto3sts

# Install ca
RUN wget "https://crt.sh/?d=2475254782" --progress=bar -O /etc/pki/ca-trust/source/anchors/ca.crt \
    && update-ca-trust \
    && update-ca-trust force-enable

# Install 
RUN pip3 install --no-cache-dir -U \
    mahotas==1.4.12 \
    scikit-image==0.17.2 \
    scikit-learn==0.24.2 \
    scipy==1.5.4 \
    jedi-language-server==0.21.0 \
    metakernel==0.28.2 \
    && pip3 install --no-cache-dir -U git+https://github.com/gmazzitelli/cygno_repo.git

# Force default python in jupyter kernel to Python3
COPY lab/kernel.json /usr/local/share/jupyter/kernels/python3/

# cmake3 alias
RUN ln -s /usr/bin/cmake3 /usr/bin/cmake

# Link folders
RUN mkdir -p ${JUPYTER_ROOT} \
    && ln -s /s3 ${JUPYTER_ROOT}/cloud-storage \
    && ln -s /shared ${JUPYTER_ROOT}/shared \
    && ln -s /private ${JUPYTER_ROOT}/private


WORKDIR /jupyter-workspace
