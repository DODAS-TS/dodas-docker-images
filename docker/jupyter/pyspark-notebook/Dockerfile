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
ENV SPARK_OPTS --driver-java-options=-Xms1024M --driver-java-options=-Xmx4096M --driver-java-options=-Dlog4j.logLevel=info

USER $NB_UID

# Install pyarrow
RUN conda install --quiet -y 'pyarrow' && \
    conda clean --all -f -y && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

USER root

RUN wget https://mirror.nohup.it/apache/spark/spark-2.4.5/spark-2.4.5-bin-hadoop2.7.tgz

RUN mkdir spark_source && cd spark_source && tar -xzvf ../spark-2.4.5-bin-hadoop2.7.tgz && rm -fr ../spark-2.4.5-bin-hadoop2.7.tgz

RUN mkdir /usr/local/spark && mv spark_source/spark-2.4.5-bin-hadoop2.7/* /usr/local/spark/

RUN sed -ie "s/\/python\/pyspark\/shell.py/\/python\/lib\/pyspark\/shell.py/" /usr/local/spark/bin/pyspark

RUN cd /usr/local/spark/python/lib && unzip -o /usr/local/spark/python/lib/pyspark.zip

RUN cd /usr/local && ln -s spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} spark

COPY minio_jars/* /usr/local/spark/jars/

# RSpark config
#ENV R_LIBS_USER $SPARK_HOME/R/lib
#RUN fix-permissions $R_LIBS_USER

# R pre-requisites
#RUN apt-get update && \
#    apt-get install -y --no-install-recommends \
#    fonts-dejavu \
#    gfortran \
#    gcc && \
#    rm -rf /var/lib/apt/lists/*

USER $NB_UID

# R packages
#RUN conda install --quiet --yes \
#    'r-base=3.6.1' \
#    'r-ggplot2=3.2*' \
#    'r-irkernel=1.0*' \
#    'r-rcurl=1.95*' \
#    'r-sparklyr=1.0*' \
#    && \
#    conda clean --all -f -y && \
#    fix-permissions $CONDA_DIR && \
#    fix-permissions /home/$NB_USER

# Apache Toree kernel
#RUN pip install --no-cache-dir \
#    https://dist.apache.org/repos/dist/release/incubator/toree/0.3.0-incubating/toree-pip/toree-0.3.0.tar.gz \
#    && \
#    jupyter toree install --sys-prefix && \
#    rm -rf /home/$NB_USER/.local && \
#    fix-permissions $CONDA_DIR && \
#    fix-permissions /home/$NB_USER

# Spylon-kernel
#RUN conda install --quiet --yes 'spylon-kernel=0.4*' && \
#    conda clean --all -f -y && \
#    python -m spylon_kernel install --sys-prefix && \
#    rm -rf /home/$NB_USER/.local && \
#    fix-permissions $CONDA_DIR && \
#    fix-permissions /home/$NB_USER


USER root
COPY start.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start.sh
COPY spark-defaults.conf /usr/local/spark/conf/spark-defaults.conf

RUN pip install jupyterlab pyspark

#RUN wget https://deb.nodesource.com/setup_14.x  -O setup_monitor
#RUN . ./setup_monitor

#RUN apt-get install -y nodejs

#RUN jupyter labextension install jupyterlab_sparkmonitor

#RUN pip install jupyterlab-sparkmonitor

#RUN jupyter serverextension enable --py sparkmonitor

WORKDIR /tmp

RUN chown $NB_UID:$NB_UID /usr/local/spark/conf/spark-defaults.conf
RUN chown $NB_UID:$NB_UID /home/jovyan/work

USER $NB_UID
WORKDIR /home/jovyan/work

ENTRYPOINT ['/usr/local/bin/start.sh', '/usr/local/spark/bin/pyspark']