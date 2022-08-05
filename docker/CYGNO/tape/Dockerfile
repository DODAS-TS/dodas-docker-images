FROM cern/cc7-base:20220601-1

RUN yum -y update && yum -y install \
    wget \
    gfal2-util \
    gfal2-all 

WORKDIR /etc/yum.repos.d

RUN  wget http://repository.egi.eu/sw/production/cas/1/current/repo-files/EGI-trustanchors.repo \
     &&  wget http://repository.egi.eu/community/software/preview.repository/2.0/releases/repofiles/centos-7-x86_64.repo 

RUN yum --setopt=tsflags=nodocs -y install epel-release yum-plugin-ovl \
    && yum --setopt=tsflags=nodocs -y install epel-release yum-plugin-ovl \
    && yum --setopt=tsflags=nodocs -y install fetch-crl wn sysstat \
    && yum clean all \
    && yum install -y ca-policy-egi-core ca-policy-lcg

#RUN fetch-crl -q

