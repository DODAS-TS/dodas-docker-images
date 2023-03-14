# Image name: dodasts/snj-base-notebook
FROM ubuntu:20.04
COPY custom.js /tmp/
WORKDIR /
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends base-files=11ubuntu5.7 libgnutls30=3.6.13-2ubuntu1.8 \
    libpam-modules=1.3.1-5ubuntu4.6 libpam-modules-bin=1.3.1-5ubuntu4.6 libpam-runtime=1.3.1-5ubuntu4.6 libpam0g=1.3.1-5ubuntu4.6 \
    libsystemd0=245.4-4ubuntu3.20 libudev1=245.4-4ubuntu3.20 tar=1.30+dfsg-7ubuntu0.20.04.3 && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y git=1:2.25.1-1ubuntu3.10 software-properties-common=0.99.9.11 \
    wget=1.20.3-1ubuntu2 fuse=2.9.9-3 --no-install-recommends \
    && apt-get clean && rm -rf /var/lib/apt/lists/* && \
    # Make dodasts folder
    mkdir -p /usr/local/share/dodasts && \
    # Make script folder
    mkdir -p /usr/local/share/dodasts/script && \
    # Make bin folder
    mkdir -p /usr/local/share/dodasts/bin && \
    DEBIAN_FRONTEND=noninteractive apt-get update \
    && apt-get install -y build-essential=12.8ubuntu1.1 python3-dev=3.8.2-0ubuntu2 python3-pip=20.0.2-5ubuntu1.8 libargon2-dev=0~20171227-0.2 \
    libffi-dev=3.3-4 libpixman-1-dev=0.38.4-0ubuntu2.1 libcairo2-dev=1.16.0-4ubuntu1 libpangox-1.0-dev=0.0.2-5ubuntu1 libjpeg-dev=8c-2ubuntu8 \
    libczmq-dev=4.2.0-2 --no-install-recommends \
    && apt-get clean && rm -rf /var/lib/apt/lists/* && \
    python3 -m pip install -U --no-cache-dir pip==23.0.1 setuptools==67.6.0 wheel==0.40.0 && \
    DEBIAN_FRONTEND=noninteractive apt-get update \
    && apt-get install -y curl libcurl4-openssl-dev=7.68.0-1ubuntu2.16 libssl-dev=1.1.1f-1ubuntu2.17 \
    dirmngr=2.2.19-3ubuntu2.2 gpg-agent=2.2.19-3ubuntu2.2 --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* && \
    # Install sts-wire
    curl -L https://github.com/DODAS-TS/sts-wire/releases/download/v2.1.2/sts-wire_linux -o /usr/local/share/dodasts/bin/sts-wire && \
    chmod +x /usr/local/share/dodasts/bin/sts-wire && \
    ln -s /usr/local/share/dodasts/bin/sts-wire /usr/local/bin/sts-wire && \
    # Install oidc-agent
    apt-key adv --keyserver hkp://pgp.surfnet.nl --recv-keys ACDFB08FDC962044D87FF00B512839863D487A87 && \
    add-apt-repository "deb https://repo.data.kit.edu/ubuntu/20.04 ./" && \
    DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y oidc-agent=4.5.1-1 && apt-get clean && rm -rf /var/lib/apt/lists/* && \
    # Install jupyterlab
    python3 -m pip install --no-cache-dir \
    jupyterlab==3.2.3 \
    ipywidgets==8.0.4 \
    jedi-language-server==0.34.8 \
    notebook==6.4.5 \
    nbdime==3.1.1 \
    pycurl==7.45.2 \
    idna==2.8 \
    importlib-metadata==6.0.0 \
    ipympl==0.9.3 && \
    curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y nodejs=16.19.1-deb-1nodesource1 && \
    python3 -m pip install --no-cache-dir jupyterhub==1.5.0 && \
    npm install -g configurable-http-proxy@4.5.4 && \
    # Add custom js for collaborative button in notebooks
    cp /tmp/custom.js "$(python3 -c "import site; print(site.getsitepackages()[0])")/notebook/static/custom/" \
    && rm /tmp/custom.js
WORKDIR /jupyter-workspace
