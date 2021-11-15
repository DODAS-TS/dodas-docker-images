# Image name: dodasts/snj-base-lab
# Image name: dodasts/snj-base-lab-gpu -> based on tensorflow/tensorflow:2.7.0rc1-gpu (with ubuntu 20:04)
ARG BASE_IMAGE="ubuntu:20.04"
FROM ${BASE_IMAGE}

RUN apt update && DEBIAN_FRONTEND=noninteractive apt upgrade -y
RUN DEBIAN_FRONTEND=noninteractive apt install -y git software-properties-common wget fuse curl

WORKDIR /

# Make dodasts, script and bin folders
RUN mkdir -p /usr/local/share/dodasts /usr/local/share/dodasts/script /usr/local/share/dodasts/bin

RUN DEBIAN_FRONTEND=noninteractive apt install -y build-essential python3-dev python3-pip libargon2-0-dev \
    libffi-dev libpixman-1-dev libcairo2-dev libpangox-1.0-dev libjpeg-dev \
    libczmq-dev libcurl4-openssl-dev libssl-dev

RUN python3 -m pip install -U pip setuptools wheel

# Install sts-wire
RUN wget https://github.com/DODAS-TS/sts-wire/releases/download/v2.0.0/sts-wire_linux -O /usr/local/share/dodasts/bin/sts-wire && \
    chmod +x /usr/local/share/dodasts/bin/sts-wire && \
    ln -s /usr/local/share/dodasts/bin/sts-wire /usr/local/bin/sts-wire

# Install oidc-agent
RUN apt-key adv --keyserver hkp://pgp.surfnet.nl --recv-keys ACDFB08FDC962044D87FF00B512839863D487A87 && \
    add-apt-repository "deb https://repo.data.kit.edu/ubuntu/20.04 ./"
RUN DEBIAN_FRONTEND=noninteractive apt update && apt install -y oidc-agent

# Install jupyterlab
RUN python3 -m pip install --no-cache-dir \
    idna==3.3 \
    importlib-metadata==4.8.2 \
    ipympl==0.8.2 \
    ipywidgets==7.6.5 \
    jedi-language-server==0.34.8 \
    jupyterlab-git==0.33.0 \
    jupyterlab-system-monitor==0.8.0 \
    jupyterlab==3.2.2 \
    nbdime==3.1.1 \
    notebook==6.4.5 \
    pycurl==7.44.1

# jupyter_http_over_ws==0.0.8 \ # Temporarly removed. Needs further config: https://github.com/googlecolab/jupyter_http_over_ws#usage
# RUN jupyter serverextension enable --py jupyter_http_over_ws

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN DEBIAN_FRONTEND=noninteractive apt install -y nodejs

RUN python3 -m pip install --no-cache-dir jupyterhub==1.5.0
RUN npm install -g configurable-http-proxy
RUN jupyter serverextension enable --py jupyterlab --sys-prefix

WORKDIR /usr/local/share/dodasts
RUN git clone https://github.com/DODAS-TS/jupyterlab-collaborative-util-extension.git \
    && cd jupyterlab-collaborative-util-extension \
    && jupyter labextension install

COPY jupyter_lab_config.py /usr/etc/jupyter/

# Build jupyter lab stuff
RUN /bin/bash -c "jupyter lab build --dev-build=False --minimize=True"

# Add Tini
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /bin/tini
RUN chmod +x /bin/tini

WORKDIR /jupyter-workspace