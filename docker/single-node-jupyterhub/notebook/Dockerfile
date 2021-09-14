# Image name: dodasts/snj-base-notebook
FROM ubuntu:20.04

ARG DEBIAN_FRONTEND noninteractive

EXPOSE 8000
EXPOSE 8888

RUN apt update && apt upgrade -y && apt install -y git

WORKDIR /

RUN apt install -y build-essential python3-dev python3-pip libargon2-0-dev \
    libffi-dev libpixman-1-dev libcairo2-dev libpangox-1.0-dev libjpeg-dev \
    libczmq-dev

RUN python3 -m pip install -U pip setuptools
RUN apt-get install -y curl libcurl4-openssl-dev libssl-dev

RUN python3 -m pip install --no-cache-dir jupyterlab==3.1.11 idna importlib-metadata
RUN python3 -m pip install --no-cache-dir notebook==6.4.1
RUN python3 -m pip install --no-cache-dir ipywidgets
RUN python3 -m pip install --no-cache-dir dockerspawner
RUN python3 -m pip install --no-cache-dir oauthenticator==0.13.0
RUN python3 -m pip install --no-cache-dir jupyterhub-idle-culler

RUN curl -fsSL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs
# RUN /bin/bash -c "jupyter lab build"

RUN python3 -m pip install --no-cache-dir jupyterhub pycurl
RUN npm install -g configurable-http-proxy

# Add custom js for collaborative button in notebooks
COPY custom.js /tmp
RUN cp /tmp/custom.js $(python3 -c "import site; print(site.getsitepackages()[0])")/notebook/static/custom/

WORKDIR /usr/share/workspace
