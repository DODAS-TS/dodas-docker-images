# Image name: dodasts/snj-base-jlabc
FROM ubuntu:20.04

RUN apt update && DEBIAN_FRONTEND=noninteractive apt upgrade -y
RUN DEBIAN_FRONTEND=noninteractive apt install -y git software-properties-common wget fuse

WORKDIR /

RUN DEBIAN_FRONTEND=noninteractive apt install -y build-essential python3-dev python3-pip libargon2-0-dev \
    libffi-dev libpixman-1-dev libcairo2-dev libpangox-1.0-dev libjpeg-dev \
    libczmq-dev

RUN python3 -m pip install -U pip setuptools
RUN DEBIAN_FRONTEND=noninteractive apt install -y curl libcurl4-openssl-dev libssl-dev

# Install sts-wire
RUN mkdir -p /usr/local/share/dodasts && \
    wget https://github.com/DODAS-TS/sts-wire/releases/download/v2.0.0/sts-wire_linux -O /usr/local/share/dodasts/sts-wire && \
    chmod +x /usr/local/share/dodasts/sts-wire && \
    ln -s /usr/local/share/dodasts/sts-wire /usr/local/bin/sts-wire

# Install oidc-agent
RUN apt-key adv --keyserver hkp://pgp.surfnet.nl --recv-keys ACDFB08FDC962044D87FF00B512839863D487A87 && \
    add-apt-repository "deb https://repo.data.kit.edu/ubuntu/20.04 ./"
RUN DEBIAN_FRONTEND=noninteractive apt update && apt install -y oidc-agent

# Install jupyterlab
RUN python3 -m pip install --no-cache-dir jupyterlab==3.1.11 idna importlib-metadata
RUN python3 -m pip install --no-cache-dir ipywidgets
RUN python3 -m pip install --no-cache-dir jedi-language-server
RUN python3 -m pip install --no-cache-dir jupyterlab-link-share

RUN curl -fsSL https://deb.nodesource.com/setup_14.x | bash -
RUN DEBIAN_FRONTEND=noninteractive apt install -y nodejs

RUN python3 -m pip install --no-cache-dir jupyterhub pycurl
RUN npm install -g configurable-http-proxy
RUN jupyter serverextension enable --py jupyterlab --sys-prefix


WORKDIR /usr/local/share/dodasts

RUN git clone https://github.com/DODAS-TS/jupyterlab-collaborative-util-extension.git \
    && cd jupyterlab-collaborative-util-extension \
    && jupyter labextension install

COPY jupyter_lab_config.py /usr/local/share/dodasts/jupyter_configs/

WORKDIR /jupyter-workspace

RUN /bin/bash -c "jupyter lab build"

CMD ["jupyter", "lab", "--debug", \
    "--JupyterApp.config_file=/usr/local/share/dodasts/jupyter_configs/jupyter_lab_config.py", \
    "--ServerApp.keyfile=/usr/local/share/dodasts/certs/jupyter/hostcert.key", \
    "--ServerApp.certfile=/usr/local/share/dodasts/certs/jupyter/hostcert.pem", \
    "--MappingKernelManager.cull_idle_timeout=10800", \
    "--MappingKernelManager.cull_connected=True"]
