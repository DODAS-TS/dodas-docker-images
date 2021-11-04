# Image name: dodasts/snj-base-lab
# Image name: dodasts/snj-base-lab-gpu -> based on tensorflow/tensorflow:2.7.0rc1-gpu (with ubuntu 20:04)
ARG BASE_IMAGE="ubuntu:20.04"
FROM ${BASE_IMAGE}

RUN apt update && DEBIAN_FRONTEND=noninteractive apt upgrade -y
RUN DEBIAN_FRONTEND=noninteractive apt install -y git software-properties-common wget fuse curl

WORKDIR /

# Make dodasts folder
RUN mkdir -p /usr/local/share/dodasts
# Make script folder
RUN mkdir -p /usr/local/share/dodasts/script
# Make bin folder
RUN mkdir -p /usr/local/share/dodasts/bin

RUN DEBIAN_FRONTEND=noninteractive apt install -y build-essential python3-dev python3-pip libargon2-0-dev \
    libffi-dev libpixman-1-dev libcairo2-dev libpangox-1.0-dev libjpeg-dev \
    libczmq-dev libcurl4-openssl-dev libssl-dev

RUN /usr/bin/python3 -m pip install --upgrade pip
RUN python3 -m pip install -U setuptools

# Install sts-wire
RUN wget https://github.com/DODAS-TS/sts-wire/releases/download/v2.0.0/sts-wire_linux -O /usr/local/share/dodasts/bin/sts-wire && \
    chmod +x /usr/local/share/dodasts/bin/sts-wire && \
    ln -s /usr/local/share/dodasts/bin/sts-wire /usr/local/bin/sts-wire

# Install oidc-agent
RUN apt-key adv --keyserver hkp://pgp.surfnet.nl --recv-keys ACDFB08FDC962044D87FF00B512839863D487A87 && \
    add-apt-repository "deb https://repo.data.kit.edu/ubuntu/20.04 ./"
RUN DEBIAN_FRONTEND=noninteractive apt update && apt install -y oidc-agent

# Install jupyterlab
RUN python3 -m pip install --no-cache-dir jupyterlab==3.1.11
RUN python3 -m pip install --no-cache-dir ipywidgets
RUN python3 -m pip install --no-cache-dir jedi-language-server
RUN python3 -m pip install --no-cache-dir notebook==6.4.1
RUN python3 -m pip install --no-cache-dir nbdime
RUN python3 -m pip install --no-cache-dir pycurl idna importlib-metadata
RUN python3 -m pip install --no-cache-dir ipympl
RUN python3 -m pip install --no-cache-dir jupyter_http_over_ws
RUN python3 -m pip install --no-cache-dir jupyterlab-git
RUN python3 -m pip install --no-cache-dir jupyterlab-system-monitor

RUN jupyter serverextension enable --py jupyter_http_over_ws

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN DEBIAN_FRONTEND=noninteractive apt install -y nodejs

RUN python3 -m pip install --no-cache-dir jupyterhub
RUN npm install -g configurable-http-proxy
RUN jupyter serverextension enable --py jupyterlab --sys-prefix

WORKDIR /usr/local/share/dodasts
RUN git clone https://github.com/DODAS-TS/jupyterlab-collaborative-util-extension.git \
    && cd jupyterlab-collaborative-util-extension \
    && jupyter labextension install

COPY jupyter_lab_config.py /usr/etc/jupyter/

RUN /bin/bash -c "jupyter lab build"

WORKDIR /jupyter-workspace