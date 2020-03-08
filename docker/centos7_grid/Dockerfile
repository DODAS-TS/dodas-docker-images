FROM centos:7

# Reference for EL7 Worker Node
# wn metapackage: https://twiki.cern.ch/twiki/bin/view/LCG/EL7WNMiddleware 

# Update system and install wget
RUN echo "LC_ALL=C" >> /etc/environment \
    && echo "LANGUAGE=C" >> /etc/environment \
    && yum --setopt=tsflags=nodocs -y update \
    && yum --setopt=tsflags=nodocs -y install wget

# Add yum repos
WORKDIR /etc/pki/rpm-gpg
RUN wget http://linuxsoft.cern.ch/wlcg/RPM-GPG-KEY-wlcg

WORKDIR /etc/yum.repos.d
RUN wget http://repository.egi.eu/community/software/preview.repository/2.0/releases/repofiles/centos-7-x86_64.repo \
    && wget http://repository.egi.eu/sw/production/cas/1/current/repo-files/EGI-trustanchors.repo \ 
    && wget http://linuxsoft.cern.ch/wlcg/wlcg-centos7.repo

WORKDIR /root

# Enable all repo, install epel-release and update yum
# - the cache is removed to free up space taken 
#   by orphaned data from disabled or removed repos
RUN yum --setopt=tsflags=nodocs -y install epel-release \
    && yum -y clean all --enablerepo=* \
    && rm -rf /var/cache/yum \
    && yum --setopt=tsflags=nodocs -y update

# Add singularity
RUN yum --setopt=tsflags=nodocs -y install singularity-runtime

# Add grid stuff
RUN yum --setopt=tsflags=nodocs -y install yum-plugin-ovl \
    && yum --setopt=tsflags=nodocs -y install fetch-crl wn

# Clean all
RUN yum clean all
