## docker build -t gitlab-registry.cern.ch/swan/docker-images/dev-jupyter .
## docker push gitlab-registry.cern.ch/swan/docker-images/dev-jupyter

FROM jupyter/minimal-notebook


MAINTAINER Diogo Castro <diogo.castro@cern.ch>
MAINTAINER Piotr Mrowczynski <piotr.mrowczynski@cern.ch>

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

COPY ./jupyterhub-singleuser /opt/conda/bin/jupyterhub-singleuser

RUN chmod +x /opt/conda/bin/jupyterhub-singleuser

USER $NB_UID

RUN pip install jupyterhub-kubespawner oauthenticator

WORKDIR /home/$NB_USER/SWAN_projects
RUN mkdir -p .init
COPY hub_config.py ./.init/jupyterhub_config.py
COPY ./sts-wire ./.init/sts-wire
COPY ./spawn.sh ./.init/spawn.sh
RUN sudo chown -R $NB_USER .init

CMD ["/usr/bin/start.sh", "jupyterhub"]
