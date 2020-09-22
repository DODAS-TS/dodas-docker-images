FROM dciangot/dodas-iam-client-rec:test5 as REGISTRATION

FROM jupyter/minimal-notebook:612aa5710bf9

MAINTAINER Diego Ciangottini <diego.ciangottini@cern.ch>


# callback = os.environ["OAUTH_CALLBACK_URL"]
# iam_server = os.environ["OAUTH_ENDPOINT"]
# IAM_ENABLED
# PASSWD
# S3_HOST
# S3_ENABLED

USER root

RUN apt-get update

# Install required apt packages for all the extensions
RUN apt-get -y install vim sudo git curl

RUN echo "jovyan ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Use bash instead of dash
RUN rm /bin/sh && \
    ln -s /bin/bash /bin/sh

USER $NB_UID

RUN pip install jupyterhub-kubespawner oauthenticator

RUN mkdir -p .init
COPY hub_config.py ./.init/jupyterhub_config.py

# COPY self registration da docker
COPY --from=REGISTRATION /usr/local/bin/dodas-IAMClientRec ./.init/dodas-IAMClientRec

RUN sudo chown -R $NB_USER .init

CMD ["/usr/bin/start.sh", "jupyterhub"]
