FROM htcondor/execute:8.9.9-el7

COPY environment /etc

ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN localedef -i en_US -c -f UTF-8 en_US.UTF-8

RUN yum update -y
RUN yum install -y centos-release-scl
RUN yum install -y sqlite-devel \
    autoconf \
    automake \
    binutils \
    bzip2-devel \
    cfitsio-devel \
    clang \
    clang-devel \
# cmake \ # Too old: 2.8 | min required 3.9
    # Install gcc7 with devtoolset-7
    chromium \
    devtoolset-7 \
    emacs \
    fftw3-devel \
    gcc \
    gcc-c++ \
    gcc-gfortran \
    git \
    graphviz-devel \
    giflib-devel \
    gsl-devel \
    glew-devel \
    libtiff-devel \
    libjpeg-devel \
    libpng-devel \
    libSM-devel \
    libX11-devel \
    libXdmcp-devel \
    libXext-devel \
    libXft-devel \
    libXpm-devel \
    libXrender-devel \
    libXt-devel \
    libxml2-devel \
    make \
    mesa-libGL-devel \
    ncurses-devel \
    openssl-devel \
    patch \
    perl \
    pcre-devel \
    perl-ExtUtils-MakeMaker \
    python3 \
    python3-devel \
    python3-pip \
    python3-numpy \
    readline-devel \
    sqlite-devel \
    sudo \
    tar \
    vim \
    wget \
    which \
    xorg-x11-server-devel \
    zlib-devel && \
    yum clean all && \
    rm -rf /var/cache/yum

# Install cmake
WORKDIR /usr/local/share

RUN wget https://github.com/Kitware/CMake/releases/download/v3.21.1/cmake-3.21.1.tar.gz && \
    tar xzvf cmake-3.21.1.tar.gz && cd cmake-3.21.1 && \
    ./bootstrap && make && make install

# Install vdt
RUN git clone https://github.com/dpiparo/vdt.git && cd vdt \
    && cmake . && make && make install

# Install root6 with dask
RUN mkdir root6build root6
RUN git clone --branch distrdf-dask https://github.com/vepadulano/root.git root6source

WORKDIR /usr/local/share/root6source

WORKDIR /usr/local/share/root6build

# Use root compiler
# RUN cmake \
#         -DCMAKE_INSTALL_PREFIX=/usr/local/share/root6 \
#         -DPython3_EXECUTABLE=/usr/bin/python3 /usr/local/share/root6source

# Use devtoolset-7 compiler
RUN cmake \
        -DCMAKE_C_COMPILER=/opt/rh/devtoolset-7/root/usr/bin/gcc \
        -DCMAKE_CXX_COMPILER=/opt/rh/devtoolset-7/root/usr/bin/g++ \
        -DCMAKE_INSTALL_PREFIX=/usr/local/share/root6 \
        -DPython3_EXECUTABLE=/usr/bin/python3 \
        /usr/local/share/root6source
# Compile root
RUN cmake --build . --target install -- -j8

ENV PYTHONPATH=/usr/local/share/root6/lib

WORKDIR /usr/local/share

# Install jupyterhub stuff
RUN curl -sL https://rpm.nodesource.com/setup_14.x | sudo bash -
RUN yum update -y && \
    yum install -y nodejs && \
    yum clean all && \
    rm -rf /var/cache/yum
RUN npm install -g configurable-http-proxy

# Dask and jupyterhub
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade setuptools
RUN python3 -m pip install dask \
    dask_jobqueue \
    click==7.1.2 \
    numpy \
    bokeh \
    ipython \
    jupyterhub \
    jupyterlab \
    notebook \
    jupyter-server-proxy \
    ipywidgets
RUN python3 -m pip install "dask[dataframe]"
RUN rm -r /root/.cache

# Install oidc-agent
RUN yum update -y && \
    yum install -y jq \
        yad \
        libmicrohttpd \
        libseccomp \
        libsecret \
        libsodium && \
    yum clean all && \
    rm -rf /var/cache/yum
RUN wget https://github.com/indigo-dc/oidc-agent/releases/download/v4.1.1/oidc-agent-4.1.1-1.el7.x86_64.rpm && \
    rpm -i oidc-agent-4.1.1-1.el7.x86_64.rpm

ARG JUPYTER_ROOT=/workarea

WORKDIR ${JUPYTER_ROOT}

COPY jupyterhub-singleuser /usr/local/bin/jupyterhub-singleuser

RUN yum update -y && \
    yum install -y fuse && \
    yum clean all && \
    rm -rf /var/cache/yum
RUN chmod +x /usr/local/bin/jupyterhub-singleuser

# Install sts-wire
RUN mkdir -p /.init && \
    wget https://github.com/DODAS-TS/sts-wire/releases/download/v2.1.2/sts-wire_linux -O /.init/sts-wire && \
    chmod +x /.init/sts-wire

# RUN mkdir ${JUPYTER_ROOT}
RUN ln -s /s3 ${JUPYTER_ROOT}/cloud-storage && \
    ln -s /opt/user_data ${JUPYTER_ROOT}/local && \
    ln -s ${JUPYTER_ROOT} /root/workarea

# ----- HTCondor -----
# RUN curl -fsSL https://get.htcondor.org | /bin/bash -s -- --download && \
# tar -x -f condor.tar.gz && \
# mv condor-*stripped condor && \
# rm condor.tar.gz && \
# cd condor && \
# ./bin/make-personal-from-tarball && \

# If root
# RUN curl -fsSL https://get.htcondor.org | /bin/bash -s --

# Download the ca.crt
RUN wget https://gist.githubusercontent.com/dciangot/018e797887cf7eadc8e4dca0b94819d3/raw/7c01f77115ff323b2248feded125c72934775bd5/ca-dodas.crt -O $HOME/.ca.crt

WORKDIR /root

COPY htc.rc .

# Install DASK jobqueue
RUN pip3 install dask-remote-jobqueue==v0.4.8

# Old approach
# RUN python3 -m pip install dask-labextension "dask[dataframe]"
# COPY labextension.yaml /usr/local/lib/python3.6/site-packages/dask_labextension/labextension.yaml
RUN python3 -m pip install jupyter-packaging \
    && git clone --branch custom_clusters https://github.com/DODAS-TS/dask-labextension.git \
    && cd dask-labextension \
    && python3 -m pip install .

COPY spawn.sh /.init/spawn.sh

RUN chmod +x /.init/spawn.sh
RUN echo "source ~/htc.rc" >>~/.bashrc
COPY kernel.json /usr/local/share/jupyter/kernels/python3/kernel.json
