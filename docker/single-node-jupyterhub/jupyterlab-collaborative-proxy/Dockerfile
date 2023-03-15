# Image name: dodasts/snj-base-jlabc-proxy
FROM ubuntu:20.04

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y --no-install-recommends && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3-dev=3.8.2-0ubuntu2 python3-pip=20.0.2-5ubuntu1.8 \
    libcurl4-openssl-dev=7.68.0-1ubuntu2.16 libssl-dev=1.1.1f-1ubuntu2.17 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/share/collab_proxy

RUN python3 -m pip install -U --no-cache-dir pip==23.0.1 setuptools==67.6.0 wheel==0.40.0 && \
    pip3 install flask==2.0.2 \
    jupyterhub==1.5.0

COPY collab_proxy.py .

CMD ["python3", "collab_proxy.py"]
