FROM htcondor/execute:8.9.9-el7

RUN python3 -m pip install -U pip setuptools

RUN pip3 install dask-remote-jobqueue==v0.4.16.dev0 jupyter-server-proxy dask \
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

RUN yum update -y && \
    yum install -y jq \
        yad \
        libmicrohttpd \
        libseccomp \
        libsecret \
        libsodium && \
        git make cmake3 gcc-c++ gcc binutils libX11-devel libXpm-devel libXft-devel libXext-devel python openssl-devel && \
    yum clean all && \
    rm -rf /var/cache/yum
RUN wget https://github.com/indigo-dc/oidc-agent/releases/download/v4.1.1/oidc-agent-4.1.1-1.el7.x86_64.rpm && \
    rpm -i oidc-agent-4.1.1-1.el7.x86_64.rpm
# RUN pip3 install jupyter-packaging
# RUN git clone --branch custom_clusters https://github.com/DODAS-TS/dask-labextension.git \
#     && cd dask-labextension \
#     && python3 -m pip install .

# COPY spawn.sh /.init/spawn.sh
# RUN echo "source ~/htc.rc" >> ~/.bashrc
# COPY kernel.json /usr/local/share/jupyter/kernels/python3/kernel.json
