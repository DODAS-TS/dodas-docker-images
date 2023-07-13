FROM jupyter/docker-stacks-foundation:ubuntu-22.04

MAINTAINER Diego Ciangottini <diego.ciangottini@cern.ch> \
           Marco Verlato <verlato@infn.it>

USER root

ARG SPARK_BASE=/usr/local
ARG SPARK_HOME=/usr/local/spark
ARG PYTHONVER=python3.11

RUN apt-get -qq update && apt-get -qq -y install vim sudo git curl openjdk-11-jdk groovy && echo "jovyan ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    rm /bin/sh && ln -s /bin/bash /bin/sh && curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash && apt-get -qq install -y nodejs && \
    rm -rf /var/lib/apt/lists/* 

RUN printf "[global] \
\nno-cache-dir = True \
" > /etc/pip.conf && \
    pip -q install jupyterhub==4.0.1 && pip -q install sparkmonitor==2.1.1 && ipython profile create --ipython-dir=.ipython && \
    jupyter nbextension install sparkmonitor --py && jupyter nbextension enable sparkmonitor --py && \
    pip -q install sparkconnector==2.4.6 && jupyter nbextension install sparkconnector --py && jupyter nbextension enable sparkconnector --py && \
    jupyter lab build && jupyter labextension list

ADD  configuration.py portallocator.py __init__.py /opt/conda/lib/${PYTHONVER}/site-packages/sparkconnector/
COPY jupyterhub-singleuser /opt/conda/bin/jupyterhub-singleuser

RUN chmod +x /opt/conda/bin/jupyterhub-singleuser && jupyter serverextension enable --py sparkconnector &&  mkdir -p /home/$NB_USER/SWAN_projects/.init && \
    echo "c.InteractiveShellApp.extensions.append('sparkmonitor.kernelextension')" >>  /home/$NB_USER/.ipython/profile_default/ipython_kernel_config.py && \
    echo "c.InteractiveShellApp.extensions.append('sparkconnector.connector')" >>  /home/$NB_USER/.ipython/profile_default/ipython_kernel_config.py && \
    printf "import os \
\nc = get_config() \
\nc.NotebookApp.ip = '0.0.0.0' \
\nc.NotebookApp.port = 8888 \
\nc.NotebookApp.open_browser = False \
\nc.InteractiveShellApp.extensions.append('sparkmonitor.kernelextension') \
\nc.InteractiveShellApp.extensions.append('sparkconnector.connector') \
\nif \"JUPYTER_TOKEN\" in os.environ: \
\n    c.NotebookApp.token = os.environ[\"JUPYTER_TOKEN\"] \
" > /home/$NB_USER/.jupyter/jupyter_notebook_config.py

WORKDIR ${SPARK_BASE}
RUN wget -nv -qO- https://downloads.apache.org/spark/spark-3.4.1/spark-3.4.1-bin-hadoop3.tgz | tar zx && mv spark-3.4.1-bin-hadoop3 spark

ADD  https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.99/aws-java-sdk-bundle-1.12.99.jar \
     https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar ${SPARK_HOME}/jars/

COPY spark-defaults.conf ${SPARK_HOME}/conf/spark-defaults.conf
COPY spawn.sh /home/$NB_USER/SWAN_projects/.init/spawn.sh

RUN wget -nv https://github.com/DODAS-TS/sts-wire/releases/download/v2.1.2/sts-wire_linux -O /home/$NB_USER/SWAN_projects/.init/sts-wire && \
    chmod +x /home/$NB_USER/SWAN_projects/.init/sts-wire && apt-get -qq update && apt-get -qq install -y software-properties-common gnupg xvfb && \
    apt-key adv --keyserver hkp://pgp.surfnet.nl --recv-keys ACDFB08FDC962044D87FF00B512839863D487A87 && \
    add-apt-repository "deb http://repo.data.kit.edu/ubuntu/jammy ./" && apt-get -qq update && apt-get -qq install -y oidc-agent fuse && \
    chown -R $NB_UID:$NB_GID /home/$NB_USER/ ${SPARK_HOME}/ && rm -rf /var/lib/apt/lists/*

USER $NB_USER
WORKDIR /home/$NB_USER/SWAN_projects
ENV SPARK_HOME=/usr/local/spark \
    PYTHONPATH=${SPARK_HOME}/python:${SPARK_HOME}/python/lib/py4j-0.10.9.7-src.zip:${PYTHONPATH} \
    SPARK_OPTS=" --driver-java-options=-Xms1024M --driver-java-options=-Xmx1024M --driver-java-options=-Dlog4j.logLevel=debug"

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
