FROM ghcr.io/dodas-ts/dodas-iam-client-rec:v0.0.6 as REGISTRATION

FROM jupyter/base-notebook:lab-4.0.2

MAINTAINER Diego Ciangottini <diego.ciangottini@cern.ch> \
           Marco Verlato <verlato@infn.it>

# callback = os.environ["OAUTH_CALLBACK_URL"]
# iam_server = os.environ["OAUTH_ENDPOINT"]
# IAM_ENABLED
# PASSWD
# S3_HOST
# S3_ENABLED

USER root

# Install required apt packages for all the extensions and use bash instead of dash
RUN echo "jovyan ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && rm /bin/sh && ln -s /bin/bash /bin/sh && \
    printf "[global] \
    \nno-cache-dir = True \
    " > /etc/pip.conf

USER $NB_UID

RUN pip -q install jupyterhub-kubespawner==6.0.0 oauthenticator==15.1.0 && mkdir -p .init

COPY hub_config.py ./.init/jupyterhub_config.py

# COPY self registration da docker
COPY --from=REGISTRATION /usr/local/bin/dodas-IAMClientRec ./.init/dodas-IAMClientRec

RUN sudo chown -R $NB_UID:$NB_GID ./

CMD ["/usr/local/bin/start.sh", "jupyterhub"]
