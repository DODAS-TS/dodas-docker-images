FROM htcondor/execute:8.9.9-el7

COPY environment /etc

ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN localedef -i en_US -c -f UTF-8 en_US.UTF-8


WORKDIR /usr/local/share

# Install jupyterhub stuff
RUN curl -sL https://rpm.nodesource.com/setup_14.x | bash -
RUN yum update -y && \
    yum install -y nodejs && \
    yum clean all && \
    rm -rf /var/cache/yum
RUN npm install -g configurable-http-proxy

# Install oidc-agent
RUN yum update -y && \
    yum install -y jq \
        yad \
        libmicrohttpd \
        libseccomp \
        libsecret \
        libsodium && \
    yum clean all && \
    rm -rf /var/cache/yum
RUN wget https://github.com/indigo-dc/oidc-agent/releases/download/v4.1.1/oidc-agent-4.1.1-1.el7.x86_64.rpm && \
    rpm -i oidc-agent-4.1.1-1.el7.x86_64.rpm

ARG JUPYTER_ROOT=/workarea

WORKDIR ${JUPYTER_ROOT}

COPY jupyterhub-singleuser /usr/local/bin/jupyterhub-singleuser

RUN yum update -y && \
    yum install -y fuse && \
    yum clean all && \
    rm -rf /var/cache/yum
RUN chmod +x /usr/local/bin/jupyterhub-singleuser

# Install sts-wire
RUN mkdir -p /.init && \
    wget https://github.com/DODAS-TS/sts-wire/releases/download/v2.0.0/sts-wire_linux -O /.init/sts-wire && \
    chmod +x /.init/sts-wire

# RUN mkdir ${JUPYTER_ROOT}
RUN ln -s /s3 ${JUPYTER_ROOT}/cloud-storage && \
    ln -s /opt/user_data ${JUPYTER_ROOT}/local && \
    ln -s ${JUPYTER_ROOT} /root/workarea

# ----- HTCondor -----
# RUN curl -fsSL https://get.htcondor.org | /bin/bash -s -- --download && \
# tar -x -f condor.tar.gz && \
# mv condor-*stripped condor && \
# rm condor.tar.gz && \
# cd condor && \
# ./bin/make-personal-from-tarball && \

# If root
# RUN curl -fsSL https://get.htcondor.org | /bin/bash -s --

# Download the ca.crt
RUN wget https://gist.githubusercontent.com/dciangot/018e797887cf7eadc8e4dca0b94819d3/raw/7c01f77115ff323b2248feded125c72934775bd5/ca-dodas.crt -O $HOME/.ca.crt

WORKDIR /root

COPY htc.rc .

COPY spawn.sh /.init/spawn.sh

RUN chmod +x /.init/spawn.sh
RUN echo "source ~/htc.rc" >>~/.bashrc
COPY kernel.json /usr/local/share/jupyter/kernels/python3/kernel.json
