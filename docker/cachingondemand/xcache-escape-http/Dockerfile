FROM dodasts/dodas-x509 as GETCERTS

FROM centos:7

ENV XRD_VERSION=4.11.2 
ENV XRD_HOST=localhost
ENV REDIR_HOST=localhost
ENV REDIR_CMSD_PORT=3113
ENV CACHE_LOG_LEVEL=info
ENV CACHE_HTTP_PORT=8443
ENV ORIGIN_HOST=https://myorigin.com
ENV ORIGIN_XRD_PORT=8443
ENV STREAMS=256
ENV LOW_WM=0.85
ENV HI_WM=0.95
ENV CACHE_RAM_GB=6
ENV BLOCK_SIZE=512k
ENV N_PREFETCH=0
ENV CACHE_PATH=/data

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

RUN yum install -y xrootd-server-$XRD_VERSION  

RUN yum -y install https://repo.opensciencegrid.org/osg/3.4/osg-3.4-el7-release-latest.rpm 
RUN yum install -y xrootd-scitokens scitokens-cpp xrootd-multiuser sudo

RUN yum install -y xrootd-devel-$XRD_VERSION xrootd-server-devel-$XRD_VERSION scitokens-cpp-devel gcc-c++ rpm-build xrdcl-http

RUN git clone https://github.com/bbockelm/xrootd-scitokens /root/xrootd-scitokens

WORKDIR /root/xrootd-scitokens

RUN git checkout fix_apply_retval \
       && mkdir -p /root/rpmbuild/SOURCES \
       && git archive fix_apply_retval --prefix=xrootd-scitokens-1.1.0/ | gzip -7 > /root/rpmbuild/SOURCES/xrootd-scitokens-1.1.0.tar.gz
RUN rpmbuild -bb rpm/xrootd-scitokens.spec \
       && yum install -y /root/rpmbuild/RPMS/x86_64/xrootd-scitokens-1.1.0-1.el7.x86_64.rpm

COPY config/* /etc/xrootd/

COPY  config/client.plugins.d/* /etc/xrootd/client.plugins.d/

RUN chown -R xrootd: /etc/xrootd/

COPY --from=0 /usr/local/bin/dodas-x509 /usr/local/bin/dodas-x509

RUN chmod +x /usr/local/bin/dodas-x509

RUN mkdir -p /data && chown -R xrootd: /data

RUN mkdir -p /xrd /var/run/xrootd && chown -R xrootd: /xrd /var/run/xrootd

COPY scripts/* /xrd/

RUN chmod -R +x /xrd/

COPY ca/DODAS.pem /etc/grid-security/certificates/DODAS.pem
COPY ca/DODAS.key /etc/grid-security/certificates/DODAS.key

COPY ca/DODAS.pem /etc/pki/ca-trust/source/anchors/DODAS.pem

RUN update-ca-trust extract

WORKDIR /xrd

ENTRYPOINT ["/xrd/start.sh"]
