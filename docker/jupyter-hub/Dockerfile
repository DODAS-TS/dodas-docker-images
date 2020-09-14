## docker build -t gitlab-registry.cern.ch/swan/docker-images/dev-jupyter .
## docker push gitlab-registry.cern.ch/swan/docker-images/dev-jupyter
FROM dciangot/dodas-iam-client-rec:test5 as REGISTRATION

FROM jupyter/minimal-notebook


MAINTAINER Diogo Castro <diogo.castro@cern.ch>
MAINTAINER Piotr Mrowczynski <piotr.mrowczynski@cern.ch>

# callback = os.environ["OAUTH_CALLBACK_URL"]
# iam_server = os.environ["OAUTH_ENDPOINT"]
# IAM_ENABLED
# PASSWD
# S3_HOST
# S3_ENABLED

USER root

RUN apt-get update

# Install required apt packages for all the extensions
RUN apt-get -y install vim sudo git curl openjdk-8-jdk

RUN echo "jovyan ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Use bash instead of dash
RUN rm /bin/sh && \
    ln -s /bin/bash /bin/sh

# Add projects folder and fix permissions
RUN mkdir /home/$NB_USER/SWAN_projects && \
    fix-permissions /home/$NB_USER

RUN apt-get install -y  fuse

COPY jupyterhub-singleuser /opt/conda/bin/jupyterhub-singleuser

RUN chmod +x /opt/conda/bin/jupyterhub-singleuser

USER $NB_UID

RUN pip install jupyterhub-kubespawner oauthenticator

WORKDIR /home/$NB_USER/SWAN_projects
RUN mkdir -p .init
COPY hub_config.py ./.init/jupyterhub_config.py

# TODO: copy from official docker image sts-wire
COPY ./sts-wire ./.init/sts-wire

# COPY self registration da docker
COPY --from=REGISTRATION /usr/local/bin/dodas-IAMClientRec ./.init/dodas-IAMClientRec

COPY ./spawn.sh ./.init/spawn.sh
RUN sudo chown -R $NB_USER .init

CMD ["/usr/bin/start.sh", "jupyterhub"]
