# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG BASE_CONTAINER=jupyter/scipy-notebook
FROM $BASE_CONTAINER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

USER root

# Spark dependencies
ENV APACHE_SPARK_VERSION 2.4.5
ENV HADOOP_VERSION 2.7

RUN apt-get -y update && \
    apt-get install --no-install-recommends -y openjdk-8-jre-headless ca-certificates-java && \
    rm -rf /var/lib/apt/lists/*

# Spark and Mesos config
ENV SPARK_HOME /usr/local/spark
ENV PYTHONPATH $SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.7-src.zip
ENV MESOS_NATIVE_LIBRARY /usr/local/lib/libmesos.so
ENV SPARK_OPTS --driver-java-options=-Xms1024M --driver-java-options=-Xmx4096M --driver-java-options=-Dlog4j.logLevel=debug

USER $NB_UID

# Install pyarrow
RUN conda install --quiet -y 'pyarrow' && \
    conda clean --all -f -y && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

USER root

RUN pip install jupyterlab pyspark

RUN wget https://deb.nodesource.com/setup_12.x  -O setup_monitor
RUN . ./setup_monitor

RUN apt-get install -y nodejs

#RUN jupyter labextension install jupyterlab_sparkmonitor
#RUN pip install jupyterlab-sparkmonitor
#RUN jupyter serverextension enable --py sparkmonitor
#RUN chown -R  $NB_UID /opt/conda/share/jupyter/

COPY ./dist  /usr/local/spark/dist
RUN mv /usr/local/spark/dist/*  /usr/local/spark
RUN rm -r /usr/local/spark/dist
COPY minio_jars/* /usr/local/spark/jars/

RUN apt install -y sudo

RUN echo "jovyan ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

RUN apt install -y yarn scala vim \
       && echo "deb https://dl.bintray.com/sbt/debian /" > /etc/apt/sources.list.d/sbt.list \
       && sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2EE0EA64E40A89B84B2DF73499E82A75642AC823 \
       && apt-get update \
       && apt-get install sbt -y

COPY start.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start.sh
COPY spark-defaults.conf /usr/local/spark/conf/spark-defaults.conf

WORKDIR /tmp

RUN chown $NB_UID:$NB_UID /usr/local/spark/conf/spark-defaults.conf \
       && chown $NB_UID:$NB_UID /home/jovyan/work


USER $NB_UID

WORKDIR /home/jovyan

RUN git clone https://gitlab.cern.ch/swan/jupyter.git \
       && cd jupyter/SparkMonitor/ \
       && cp -r js sparkmonitor/ \
       && make \
       && pip install . \
       && jupyter nbextension install --py sparkmonitor --user --symlink \
       && jupyter nbextension enable sparkmonitor --user --py \
       && jupyter serverextension enable --py --user sparkmonitor \
       && ipython profile create \
       && echo "c.InteractiveShellApp.extensions.append('sparkmonitor.kernelextension')" >>  $(ipython profile locate default)/ipython_kernel_config.py
#RUN ipython profile create --ipython-dir=.ipython \
#       && echo "c.InteractiveShellApp.extensions.append('sparkmonitor.kernelextension')" >>  .ipython/profile_default/ipython_config.py

WORKDIR /home/jovyan/work

ENTRYPOINT ['/usr/local/bin/start.sh', '/usr/local/spark/bin/pyspark']