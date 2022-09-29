FROM cern/cc7-base:20220601-1

WORKDIR /etc/yum.repos.d

RUN yum -y update && yum -y install \
    wget 

RUN  wget http://repository.egi.eu/sw/production/cas/1/current/repo-files/EGI-trustanchors.repo \
     &&  wget http://repository.egi.eu/community/software/preview.repository/2.0/releases/repofiles/centos-7-x86_64.repo \
     && wget https://repo.data.kit.edu/data-kit-edu-centos7.repo

RUN yum install -y \
    oidc-agent \
    gfal2-util \
    gfal2-all \
    && yum clean all 

RUN yum --setopt=tsflags=nodocs -y install epel-release yum-plugin-ovl \
    && yum --setopt=tsflags=nodocs -y install epel-release yum-plugin-ovl \
    && yum --setopt=tsflags=nodocs -y install fetch-crl wn sysstat \
    && yum clean all \
    && yum install -y ca-policy-egi-core ca-policy-lcg


	
WORKDIR /root
RUN sed -i 's/\/bin\/bin\//\/bin\//g' /usr/bin/oidc-agent-service
RUN wget https://raw.githubusercontent.com/gmazzitelli/dodas-docker-images/master/docker/CYGNO/tape/oicd-setup.sh
RUN wget https://raw.githubusercontent.com/gmazzitelli/dodas-docker-images/master/docker/CYGNO/tape/cygno_s32tape.sh
RUN wget https://raw.githubusercontent.com/gmazzitelli/dodas-docker-images/master/docker/CYGNO/tape/s32tape.py
RUN chmod a+x oicd-setup.sh cygno_s32tape.sh s32tape.py
