# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG BASE_CONTAINER=jupyter/scipy-notebook
FROM $BASE_CONTAINER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

USER root

# Spark dependencies
ENV APACHE_SPARK_VERSION 2.4.4
ENV HADOOP_VERSION 2.7

RUN apt-get -y update && \
    apt-get install --no-install-recommends -y openjdk-8-jre-headless ca-certificates-java && \
    rm -rf /var/lib/apt/lists/*

#RUN cd /tmp && \
#       wget -q https://mirrors.ukfast.co.uk/sites/ftp.apache.org/spark/spark-${APACHE_SPARK_VERSION}/spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz  && \
#       tar xzf spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -C /usr/local --owner root --group root --no-same-owner && \
#       rm spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz
RUN echo "test" && wget https://github.com/DODAS-TS/dodas-docker-images/archive/master.zip \
       && unzip master

RUN cp -r dodas-docker-images-master/docker/spark/spark_src /usr/local/spark \
       && rm -fr dodas-docker-images-master
#    tar xzf spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -C /usr/local --owner root --group root --no-same-owner && \
#    rm spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# Mesos dependencies
# Install from the Xenial Mesosphere repository since there does not (yet)
# exist a Bionic repository and the dependencies seem to be compatible for now.
COPY mesos.key /tmp/
RUN apt-get -y update && \
    apt-get install --no-install-recommends -y gnupg && \
    apt-key add /tmp/mesos.key && \
    echo "deb http://repos.mesosphere.io/ubuntu xenial main" > /etc/apt/sources.list.d/mesosphere.list && \
    apt-get -y update && \
    apt-get --no-install-recommends -y install mesos=1.2\* && \
    apt-get purge --auto-remove -y gnupg && \
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

#ARG BASE_CONTAINER=jupyter/pyspark-notebook
#FROM $BASE_CONTAINER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

USER root

RUN cd /usr/local && ln -s spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} spark


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

WORKDIR /tmp
#ENV SPARK_VER=${SPARK_VER:-"2.4.4"}
#ENV INTEL_SPARK_VER=${INTEL_SPARK_VER:-"2.3.1"}
#ENV INTEL_SCALA_VER=${INTEL_SCALA_VER:-"2.11.8"}
#ENV HADOOP_VER=${HADOOP_VER:-"2.7"}
#ENV BIGDL_VER=${BIGDL_VER:-"0.7.1"}
#ENV BIGDL_URI=${BIGDL_URI:-"https://repo1.maven.org/maven2/com/intel/analytics/bigdl/dist-spark-${INTEL_SPARK_VER}-scala-${INTEL_SCALA_VER}-all/${BIGDL_VER}/dist-spark-${INTEL_SPARK_VER}-scala-${INTEL_SCALA_VER}-all-${BIGDL_VER}-dist.zip"}
#ENV PYTHONPATH=${PYTHONPATH}:/usr/local/spark/python/lib/bigdl-${BIGDL_VER}-python-api.zip

#RUN mkdir intel \
#    && wget ${BIGDL_URI} -O bigdl.zip

#RUN unzip -o bigdl.zip \
#    && mv lib/*.zip /usr/local/spark/python/lib/ \
#    && mv lib/*.jar /usr/local/spark/jars/ \
#    && rm -Rf /tmp/intel


RUN chown $NB_UID:$NB_UID /usr/local/spark/conf/spark-defaults.conf
RUN chown $NB_UID:$NB_UID /home/jovyan/work

USER $NB_UID
WORKDIR /home/jovyan/work

#ENV SPARK_VER=${SPARK_VER:-"2.4.4"}
#ENV INTEL_SPARK_VER=${INTEL_SPARK_VER:-"2.3.1"}
#ENV INTEL_SCALA_VER=${INTEL_SCALA_VER:-"2.11.8"}
#ENV HADOOP_VER=${HADOOP_VER:-"2.7"}
#ENV BIGDL_VER=${BIGDL_VER:-"0.7.1"}
#ENV BIGDL_URI=${BIGDL_URI:-"https://repo1.maven.org/maven2/com/intel/analytics/bigdl/dist-spark-${INTEL_SPARK_VER}-scala-${INTEL_SCALA_VER}-all/${BIGDL_VER}/dist-spark-${INTEL_SPARK_VER}-scala-${INTEL_SCALA_VER}-all-${BIGDL_VER}-dist.zip"}
#ENV PYTHONPATH=${PYTHONPATH}:/usr/local/spark/python/lib/bigdl-${BIGDL_VER}-python-api.zip
