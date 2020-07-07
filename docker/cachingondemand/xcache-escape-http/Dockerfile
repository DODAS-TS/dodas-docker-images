FROM dodasts/dodas-x509 as GETCERTS

#FROM centos:7
FROM opensciencegrid/software-base:fresh


ENV XRD_VERSION=4.12.3
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

WORKDIR /etc/yum.repos.d

RUN yum install -y wget
#RUN wget http://repository.egi.eu/sw/production/cas/1/current/repo-files/EGI-trustanchors.repo
#RUN yum -y install https://repo.opensciencegrid.org/osg/3.5/osg-3.5-el7-release-latest.rpm
#RUN yum --setopt=tsflags=nodocs -y install epel-release yum-plugin-ovl \
#    && yum --setopt=tsflags=nodocs -y install fetch-crl wn sysstat git vim gcc cmake make ca-policy-egi-core ca-policy-lcg \
#           voms-clients-cpp voms \
#   && yum clean all

RUN yum update -y

RUN yum remove -y xrootd
#RUN yum install -y davix-devel gsoap-2 openssl xrdcl-http-$XRD_VERSION xrootd-server-$XRD_VERSION  xrootd-server-devel-$XRD_VERSION xrootd-devel-$XRD_VERSION xrootd-multiuser-$XRD_VERSION
RUN yum install -y davix-devel gsoap-2 openssl xrdcl-http xrootd-server xrootd-server-devel xrootd-devel xrootd-multiuser

RUN yum install -y sysstat vim  gcc make cmake gcc-c++ rpm-build git sudo

#RUN git clone https://github.com/xrootd/xrdcl-http.git /root/xrootd-http-client

WORKDIR /root/xrootd-http-client
#RUN ./packaging/makesrpm.sh && ls -altrh .

RUN yum install -y https://kojipkgs.fedoraproject.org//packages/scitokens-cpp/0.5.1/1.el7/x86_64/scitokens-cpp-0.5.1-1.el7.x86_64.rpm
RUN yum install -y https://kojipkgs.fedoraproject.org//packages/scitokens-cpp/0.5.1/1.el7/x86_64/scitokens-cpp-devel-0.5.1-1.el7.x86_64.rpm

RUN git clone https://github.com/bbockelm/xrootd-scitokens /root/xrootd-scitokens

WORKDIR /root/xrootd-scitokens

RUN git checkout fix_apply_retval \
       && mkdir -p /root/rpmbuild/SOURCES \
       && git archive fix_apply_retval --prefix=xrootd-scitokens-1.1.0/ | gzip -7 > /root/rpmbuild/SOURCES/xrootd-scitokens-1.1.0.tar.gz
RUN yum remove -y xrootd-scitokens
RUN rpmbuild -bb rpm/xrootd-scitokens.spec \
       && yum install -y /root/rpmbuild/RPMS/x86_64/xrootd-scitokens-1.1.0-1.el7.x86_64.rpm

COPY config/* /etc/xrootd/

COPY  config/client.plugins.d/* /etc/xrootd/client.plugins.d/

RUN chown -R xrootd:xrootd /etc/xrootd/


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
