FROM dodasts/dodas-x509 as GETCERTS

FROM centos:7

ENV XRD_VERSION=4.11.2 
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

RUN yum install -y xrootd-server-$XRD_VERSION  

RUN yum -y install https://repo.opensciencegrid.org/osg/3.4/osg-3.4-el7-release-latest.rpm 
RUN yum install -y xrootd-scitokens scitokens-cpp xrootd-multiuser sudo

COPY config/* /etc/xrootd/

RUN chown -R xrootd: /etc/xrootd/

COPY --from=0 /usr/local/bin/dodas-x509 /usr/local/bin/dodas-x509

RUN chmod +x /usr/local/bin/dodas-x509

RUN mkdir /data && chown -R xrootd: /data

RUN mkdir /xrd /var/run/xrootd && chown -R xrootd: /xrd /var/run/xrootd

COPY scripts/* /xrd/

RUN chmod -R +x /xrd/

WORKDIR /xrd

ENTRYPOINT ["/xrd/start.sh"]
