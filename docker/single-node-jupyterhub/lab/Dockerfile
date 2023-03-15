# Image name: dodasts/snj-base-lab
# Image name: dodasts/snj-base-lab-gpu -> based on tensorflow/tensorflow:2.7.0rc1-gpu (with ubuntu 20:04)
ARG BASE_IMAGE="ubuntu:20.04"
# hadolint ignore=DL3006
FROM ${BASE_IMAGE}

ARG BASE_IMAGE
WORKDIR /
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN if [ "$BASE_IMAGE" = "tensorflow/tensorflow:2.7.0rc1-gpu" ] ;  then \       
    rm /etc/apt/sources.list.d/cuda.list \
    && rm /etc/apt/sources.list.d/nvidia-ml.list \
    && apt-key del 7fa2af80 \
    && apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub \
    && apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/7fa2af80.pub; else echo 'Ubuntu'; fi && \
    DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y --no-install-recommends && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    git=1:2.25.1-1ubuntu3.10 software-properties-common=0.99.9.11 wget=1.20.3-1ubuntu2 fuse=2.9.9-3 curl=7.68.0-1ubuntu2.16 \
    build-essential=12.8ubuntu1.1 python3-dev=3.8.2-0ubuntu2 python3-pip=20.0.2-5ubuntu1.8 libargon2-dev=0~20171227-0.2 \
    libffi-dev=3.3-4 libpixman-1-dev=0.38.4-0ubuntu2.1 libcairo2-dev=1.16.0-4ubuntu1 libpangox-1.0-dev=0.0.2-5ubuntu1 \
    libjpeg-dev=8c-2ubuntu8 libczmq-dev=4.2.0-2 curl=7.68.0-1ubuntu2.16 libcurl4-openssl-dev=7.68.0-1ubuntu2.16 \
    libssl-dev=1.1.1f-1ubuntu2.17 dirmngr=2.2.19-3ubuntu2.2 gpg-agent=2.2.19-3ubuntu2.2 \
    && apt-get clean && rm -rf /var/lib/apt/lists/* && \
    # Make dodasts, script and bin folders
    mkdir -p /usr/local/share/dodasts /usr/local/share/dodasts/script /usr/local/share/dodasts/bin && \
    python3 -m pip install -U --no-cache-dir pip==23.0.1 setuptools==67.6.0 wheel==0.40.0 && \
    # Install sts-wire
    curl -L https://github.com/DODAS-TS/sts-wire/releases/download/v2.1.2/sts-wire_linux -o /usr/local/share/dodasts/bin/sts-wire && \
    chmod +x /usr/local/share/dodasts/bin/sts-wire && \
    ln -s /usr/local/share/dodasts/bin/sts-wire /usr/local/bin/sts-wire && \
    # Install oidc-agent
    apt-key adv --keyserver hkp://pgp.surfnet.nl --recv-keys ACDFB08FDC962044D87FF00B512839863D487A87 && \
    add-apt-repository "deb https://repo.data.kit.edu/ubuntu/20.04 ./" && \
    DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y --no-install-recommends oidc-agent=4.5.1-1 && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    # Install jupyterlab
    python3 -m pip install --no-cache-dir \
    idna==3.3 \
    importlib-metadata==4.8.2 \
    ipympl==0.8.2 \
    ipywidgets==7.6.5 \
    jedi-language-server==0.34.8 \
    jupyterlab-git==0.33.0 \
    jupyterlab-system-monitor==0.8.0 \
    jupyterlab==3.2.3 \
    nbdime==3.1.1 \
    notebook==6.4.5 \
    pycurl==7.44.1 && \
    # jupyter_http_over_ws==0.0.8 \ # Temporarly removed. Needs further config: https://github.com/googlecolab/jupyter_http_over_ws#usage
    # RUN jupyter serverextension enable --py jupyter_http_over_ws
    curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends nodejs=16.19.1-deb-1nodesource1 && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    python3 -m pip install --no-cache-dir jupyterhub==1.5.0 && \
    npm install -g configurable-http-proxy@4.5.4 && \
    jupyter serverextension enable --py jupyterlab --sys-prefix

WORKDIR /usr/local/share/dodasts
RUN git clone https://github.com/DODAS-TS/jupyterlab-collaborative-util-extension.git
WORKDIR /usr/local/share/dodasts/jupyterlab-collaborative-util-extension
RUN sed -i 's/\(    "target":\)\(.*\)/\1 "'"es2018"'",/g' tsconfig.json && \
    sed -i '/"compilerOptions": {/a \    "lib": ["es2018", "dom"],' tsconfig.json && \
    jupyter labextension install
WORKDIR /usr/local/share/dodasts

COPY jupyter_lab_config.py /usr/etc/jupyter/

# Build jupyter lab stuff
RUN /bin/bash -c "jupyter lab build --dev-build=False --minimize=True"

# Add Tini
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /bin/tini
RUN chmod +x /bin/tini

WORKDIR /jupyter-workspace
