# Image name: dodasts/snj-base-jlabc
FROM ubuntu:20.04

EXPOSE 8000
EXPOSE 8888

RUN DEBIAN_FRONTEND=noninteractive apt update && apt upgrade -y && apt install -y git

WORKDIR /

RUN DEBIAN_FRONTEND=noninteractive apt install -y build-essential python3-dev python3-pip libargon2-0-dev \
    libffi-dev libpixman-1-dev libcairo2-dev libpangox-1.0-dev libjpeg-dev \
    libczmq-dev

RUN python3 -m pip install -U pip setuptools
RUN DEBIAN_FRONTEND=noninteractive apt install -y curl libcurl4-openssl-dev libssl-dev

RUN python3 -m pip install --no-cache-dir jupyterlab==3.1.11 idna importlib-metadata
RUN python3 -m pip install --no-cache-dir jupyterlab-link-share
RUN python3 -m pip install --no-cache-dir jedi-language-server

RUN curl -fsSL https://deb.nodesource.com/setup_14.x | bash -
RUN DEBIAN_FRONTEND=noninteractive apt install -y nodejs
# RUN /bin/bash -c "jupyter lab build"

RUN python3 -m pip install --no-cache-dir jupyterhub pycurl
RUN npm install -g configurable-http-proxy
RUN jupyter serverextension enable --py jupyterlab --sys-prefix

COPY jupyterhub_config.py /etc/jupyterhub/

WORKDIR /usr/local/share/dodasts

RUN git clone https://github.com/DODAS-TS/jupyterlab-collaborative-util-extension.git \
    && cd jupyterlab-collaborative-util-extension \
    && jupyter labextension install

WORKDIR /usr/share/workspace

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--debug", \
    "--no-browser", \
    "--LabApp.collaborative=True", \
    "--ServerApp.allow_password_change=False", \
    "--ServerApp.keyfile=/usr/local/share/dodasts/certs/jupyter/hostcert.key", \
    "--ServerApp.certfile=/usr/local/share/dodasts/certs/jupyter/hostcert.pem", \
    "--MappingKernelManager.cull_idle_timeout=10800", \
    "--MappingKernelManager.cull_connected=True"]
