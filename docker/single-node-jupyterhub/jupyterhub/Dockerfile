# Image name: dodasts/snj-base-jhub

FROM jupyterhub/jupyterhub:1.5.0

RUN mkdir -p /.init

RUN python3 -m pip install --no-cache-dir -U pip setuptools wheel
RUN python3 -m pip install --no-cache-dir \
    dockerspawner==12.1.0 \
    oauthenticator==14.2.0 \
    pyjwt==2.4.0 \
    jupyterhub-idle-culler==1.2.1

# Test user
# RUN useradd test -p "$(openssl passwd -1 test)"
# RUN mkdir /home/test && chown test: /home/test

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y wget && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN wget "https://crt.sh/?d=2475254782" --progress=bar -O /usr/local/share/ca-certificates/ca.crt && update-ca-certificates

COPY jupyterhub_config.py /srv/jupyterhub/

