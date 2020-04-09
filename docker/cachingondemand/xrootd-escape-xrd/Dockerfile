FROM dodasts/dodas-x509:test as GETCERTS

FROM centos:7

ENV XRD_VERSION=4.11.3 
ENV XRD_HOST=localhost

RUN echo "LC_ALL=C" >> /etc/environment \ 
    && echo "LANGUAGE=C" >> /etc/environment \ 
    && yum --setopt=tsflags=nodocs -y update \ 
    && yum --setopt=tsflags=nodocs -y install wget \ 
    && yum clean all 

WORKDIR /etc/yum.repos.d 

RUN wget http://repository.egi.eu/sw/production/cas/1/current/repo-files/EGI-trustanchors.repo 
RUN yum --setopt=tsflags=nodocs -y install epel-release yum-plugin-ovl \ 
    && yum --setopt=tsflags=nodocs -y install fetch-crl wn sysstat git vim gcc cmake make ca-policy-egi-core ca-policy-lcg \ 
             voms-clients-cpp voms \ 
    && yum clean all 

RUN yum install -y xrootd-server-$XRD_VERSION xrootd-devel-$XRD_VERSION gcc-c++ voms-devel sudo

WORKDIR /root

RUN git clone https://github.com/gganis/vomsxrd.git /root/vomsxrd

WORKDIR /root/vomsxrd

RUN git checkout v0.8.0-rc1 \
       && mkdir -p build && cd build \
       && cmake .. -DXROOTD_LIBRARY=/lib64 -DCMAKE_INSTALL_PREFIX=/ \
       && make install

WORKDIR /root

RUN  mkdir -p /etc/vomses \
        && wget https://indigo-iam.github.io/escape-docs/voms-config/voms-escape.cloud.cnaf.infn.it.vomses -O /etc/vomses/voms-escape.cloud.cnaf.infn.it.vomses \
        && mkdir -p /etc/grid-security/vomsdir/escape \
        && wget https://indigo-iam.github.io/escape-docs/voms-config/voms-escape.cloud.cnaf.infn.it.lsc -O /etc/grid-security/vomsdir/escape/voms-escape.cloud.cnaf.infn.it.lsc

COPY config/* /etc/xrootd/

RUN chown -R xrootd: /etc/xrootd/

COPY --from=0 /usr/local/bin/dodas-x509 /usr/local/bin/dodas-x509

RUN chmod +x /usr/local/bin/dodas-x509

RUN mkdir -p /data && chown -R xrootd: /data

RUN mkdir -p /xrd /var/run/xrootd && chown -R xrootd: /xrd /var/run/xrootd

COPY scripts/* /xrd/

RUN chmod -R +x /xrd/

COPY ca/DODAS.pem /etc/grid-security/certificates/DODAS.pem
COPY ca/DODAS.key /etc/grid-security/certificates/DODAS.key

WORKDIR /xrd

ENTRYPOINT ["/xrd/start.sh"]

