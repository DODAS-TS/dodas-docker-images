# Image name: dodasts/snj-base-notebook
FROM ubuntu:20.04

RUN apt update && DEBIAN_FRONTEND=noninteractive apt upgrade -y
RUN DEBIAN_FRONTEND=noninteractive apt install -y git software-properties-common wget fuse

WORKDIR /

# Make dodasts folder
RUN mkdir -p /usr/local/share/dodasts
# Make script folder
RUN mkdir -p /usr/local/share/dodasts/script
# Make bin folder
RUN mkdir -p /usr/local/share/dodasts/bin

RUN DEBIAN_FRONTEND=noninteractive apt install -y build-essential python3-dev python3-pip libargon2-0-dev \
    libffi-dev libpixman-1-dev libcairo2-dev libpangox-1.0-dev libjpeg-dev \
    libczmq-dev

RUN python3 -m pip install -U pip setuptools wheel
RUN DEBIAN_FRONTEND=noninteractive apt install -y curl libcurl4-openssl-dev libssl-dev

# Install sts-wire
RUN wget https://github.com/DODAS-TS/sts-wire/releases/download/v2.0.0/sts-wire_linux -O /usr/local/share/dodasts/bin/sts-wire && \
    chmod +x /usr/local/share/dodasts/bin/sts-wire && \
    ln -s /usr/local/share/dodasts/bin/sts-wire /usr/local/bin/sts-wire

# Install oidc-agent
RUN apt-key adv --keyserver hkp://pgp.surfnet.nl --recv-keys ACDFB08FDC962044D87FF00B512839863D487A87 && \
    add-apt-repository "deb https://repo.data.kit.edu/ubuntu/20.04 ./"
RUN DEBIAN_FRONTEND=noninteractive apt update && apt install -y oidc-agent

# Install jupyterlab
RUN python3 -m pip install --no-cache-dir jupyterlab==3.1.11   \
    ipywidgets \
    jedi-language-server   \
    notebook==6.4.1    \
    nbdime \
    pycurl \
    idna \
    importlib-metadata \
    ipympl

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN DEBIAN_FRONTEND=noninteractive apt install -y nodejs

RUN python3 -m pip install --no-cache-dir jupyterhub==1.5.0
RUN npm install -g configurable-http-proxy

# Add custom js for collaborative button in notebooks
COPY custom.js /tmp
RUN cp /tmp/custom.js $(python3 -c "import site; print(site.getsitepackages()[0])")/notebook/static/custom/

WORKDIR /jupyter-workspace
