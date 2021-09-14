# Image name: dodasts/snj-base-jhub

FROM dciangot/dodas-iam-client-rec:test5 as REGISTRATION

FROM jupyterhub/jupyterhub:1.3

ARG DEBIAN_FRONTEND noninteractive

WORKDIR / 

RUN python3 -m pip install -U pip
RUN python3 -m pip install --no-cache-dir dockerspawner
RUN python3 -m pip install --no-cache-dir oauthenticator==0.13.0
RUN python3 -m pip install --no-cache-dir jupyterhub-idle-culler

# Test user
# RUN useradd test -p "$(openssl passwd -1 test)"
# RUN mkdir /home/test && chown test: /home/test

RUN apt-get update && apt-get install -y wget

RUN wget "https://crt.sh/?d=2475254782" -O /usr/local/share/ca-certificates/ca.crt && update-ca-certificates

RUN mkdir -p .init

COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py

# COPY self registration da docker
COPY --from=REGISTRATION /usr/local/bin/dodas-IAMClientRec ./.init/dodas-IAMClientRec
