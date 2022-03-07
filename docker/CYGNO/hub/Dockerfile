# Image name: dodasts/snj-base-jhub
FROM ghcr.io/dodas-ts/dodas-iam-client-rec:v0.0.6-pre3 as REGISTRATION

# Image name: dodasts/cygno-hub
FROM dodasts/snj-base-jhub:v1.0.0-snj

COPY --from=REGISTRATION /usr/local/bin/dodas-IAMClientRec /.init/dodas-IAMClientRec

COPY jupyterhub_config.py /srv/jupyterhub/

