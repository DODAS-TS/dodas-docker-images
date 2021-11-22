# Image name: dodasts/snj-base-jlabc-proxy
FROM ubuntu:20.04

RUN DEBIAN_FRONTEND=noninteractive apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y python3 python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/share/collab_proxy

RUN python3 -m pip install -U pip setuptools wheel
RUN pip3 install flask==2.0.2 \
    jupyterhub==1.5.0

RUN DEBIAN_FRONTEND=noninteractive apt install -y libcurl4-openssl-dev libssl-dev

COPY collab_proxy.py .

CMD ["python3", "collab_proxy.py"]
