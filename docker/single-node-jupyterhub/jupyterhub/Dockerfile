# Image name: dodasts/snj-base-jhub

FROM dciangot/dodas-iam-client-rec:test5 as REGISTRATION

FROM jupyterhub/jupyterhub:1.5.0

# COPY self registration da docker
RUN mkdir -p /.init
COPY --from=REGISTRATION /usr/local/bin/dodas-IAMClientRec /.init/dodas-IAMClientRec

RUN python3 -m pip install -U pip setuptools wheel
RUN python3 -m pip install --no-cache-dir dockerspawner==12.1.0 \
    oauthenticator==14.2.0 \
    jupyterhub-idle-culler==1.2.1

# Test user
# RUN useradd test -p "$(openssl passwd -1 test)"
# RUN mkdir /home/test && chown test: /home/test

RUN apt update && DEBIAN_FRONTEND=noninteractive apt install -y wget

RUN wget "https://crt.sh/?d=2475254782" -O /usr/local/share/ca-certificates/ca.crt && update-ca-certificates

COPY jupyterhub_config.py .

