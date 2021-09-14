# Image name: dodasts/snj-base-jlabc-proxy
FROM ubuntu:20.04

ARG DEBIAN_FRONTEND noninteractive

EXPOSE 8099

RUN apt update && apt upgrade -y && apt install -y python3 python3-pip

WORKDIR /usr/share/collab_proxy

RUN pip3 install flask
RUN pip3 install jupyterhub

RUN apt install -y libcurl4-openssl-dev libssl-dev

COPY collab_proxy.py .

CMD ["python3", "collab_proxy.py"]
