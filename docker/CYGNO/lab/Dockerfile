# Image name: dodasts/cygno-lab
FROM dodasts/snj-base-lab-cc7:v1.1.1-snj

ENV OIDC_AGENT=/usr/bin/oidc-agent

# Set python3 to default globally
# RUN update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1 \
#     && update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2 \
#     && yes 2 | update-alternatives --config python

ARG JUPYTER_ROOT=/jupyter-workspace

COPY lab/.bashrc /root/

COPY lab/jupyter_lab_config.py /tmp/
RUN cat /tmp/jupyter_lab_config.py >> /usr/etc/jupyter/jupyter_lab_config.py \
    && rm /tmp/jupyter_lab_config.py

COPY assets/packages /tmp/

COPY lab/htcondor-development-rhel7.repo /etc/yum.repos.d/
COPY lab/RPM-GPG-KEY-HTCondor /etc/pki/rpm-gpg/
COPY lab/htcondor_ca.crt /etc/pki/ca-trust/source/anchors/
COPY lab/condor_config.local /etc/condor/

# clean metadata: https://srvfail.com/yum-doesnt-work-in-clean-centos-7-install-exiting-on-user-cancel/
RUN yum -y clean metadata \
    && yum --exclude=\*oidc-agent\* -y update \
    && yum --exclude=\*oidc-agent\* -y upgrade \
    && xargs yum -y install < /tmp/packages \
    && yum -y install \
    condor \
    condor-boinc \
    condor-classads \
    condor-externals \
    condor-procd \
    python2-condor \
    python3-condor \
    && yum -y clean all \
    && rm -f /tmp/packages

RUN jupyter labextension uninstall @jlab_collaborative_ext/context-menu

COPY scripts/post_script.sh /usr/local/share/dodasts/script/
RUN chmod +x /usr/local/share/dodasts/script/post_script.sh

COPY scripts/oidc_agent_init.sh /usr/local/share/dodasts/script/
RUN chmod +x /usr/local/share/dodasts/script/oidc_agent_init.sh

WORKDIR /usr/local/share/dodasts/script/

# garfield env variables
ENV GARFIELD_HOME=/usr/local/share/garfield
ENV HEED_DATABASE=${GARFIELD_HOME}/Heed/heed++/database

# Install Geant4
COPY scripts/install_geant4.sh /usr/local/share/dodasts/script/
RUN chmod +x /usr/local/share/dodasts/script/install_geant4.sh
RUN ./install_geant4.sh
# Install garfield
COPY scripts/install_garfield.sh /usr/local/share/dodasts/script/
RUN chmod +x /usr/local/share/dodasts/script/install_garfield.sh
RUN ./install_garfield.sh
# Install CADMesh
COPY scripts/install_CADMesh.sh /usr/local/share/dodasts/script/
RUN chmod +x /usr/local/share/dodasts/script/install_CADMesh.sh
RUN ./install_CADMesh.sh
# Install RooUnfold
COPY scripts/install_RooUnfold.sh /usr/local/share/dodasts/script/
RUN chmod +x /usr/local/share/dodasts/script/install_RooUnfold.sh
RUN ./install_RooUnfold.sh
# Install CYGNO-MC
COPY scripts/install_CYGNO-MC.sh /usr/local/share/dodasts/script/
RUN chmod +x /usr/local/share/dodasts/script/install_CYGNO-MC.sh
RUN ./install_CYGNO-MC.sh

WORKDIR /

# Install boto
RUN pip3 install --no-cache-dir -U git+https://github.com/DODAS-TS/boto3sts

# Install ca
RUN wget "https://crt.sh/?d=2475254782" --progress=bar -O /etc/pki/ca-trust/source/anchors/ca.crt \
    && update-ca-trust \
    && update-ca-trust force-enable

# Install 
RUN pip3 install --no-cache-dir -U \
    mahotas==1.4.11 \
    scikit-image==0.17.2 \
    scikit-learn==0.24.2 \
    scipy==1.5.4 \
    seaborn==0.11.2 \
    jedi-language-server==0.21.0 \
    metakernel==0.28.2 \
    tensorflow==2.6.2 \
    opencv-python==4.6.0.66 \
    root_numpy \
    pydot \
    graphviz \
    uproot \
    && pip3 install --no-cache-dir -U git+https://github.com/CYGNUS-RD/cygno.git \
    && pip3 install 'https://github.com/CYGNUS-RD/middleware/blob/master/midas/midaslib.tar.gz?raw=true'

# Force default python in jupyter kernel to Python3
COPY lab/kernel.json /usr/local/share/jupyter/kernels/python3/

# cmake3 alias
RUN ln -s /usr/bin/cmake3 /usr/bin/cmake

# last requirments....
RUN yum install emacs -y 
RUN yum install screen -y
RUN wget https://www.python.org/ftp/python/3.9.10/Python-3.9.10.tgz; \
    tar xvf Python-3.9.10.tgz; \
    cd Python-3.9*/; \
    ./configure --enable-optimizations; \
    make altinstall; \
    cd .. ; \
    rm -rf Python-3.9*

# Link folders
RUN mkdir -p ${JUPYTER_ROOT} \
    && ln -s /s3 ${JUPYTER_ROOT}/cloud-storage \
    && ln -s /shared ${JUPYTER_ROOT}/shared \
    && ln -s /private ${JUPYTER_ROOT}/private


WORKDIR /jupyter-workspace
