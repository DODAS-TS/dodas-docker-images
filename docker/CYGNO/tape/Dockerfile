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

RUN wget https://repo.data.kit.edu/data-kit-edu-centos7.repo
RUN yum -y update && yum -y install \
	git \
	oidc-agent
	
RUN sed -i 's/\/bin\/bin\//\/bin\//g' /usr/bin/oidc-agent-service

#
# RUN echo "eval `oidc-agent-service use`" >> /root/.bash_profile
# RUN echo "oidc-gen --issuer https://iam-t1-computing.cloud.cnaf.infn.it/ --pw-cmd=\"echo pwd\" --scope \"openid profile email address phone offline_access eduperson_scoped_affiliation eduperson_entitlement\" t1-tape"  >> /root/.bash_profile 
# RUN echo "export BEARER_TOKEN=$(oidc-token t1-tape)"  >> /root/.bash_profile 
# RUN echo "echo \"Tocken t1-tape: $BEARER_TOKEN\""  >> /root/.bash_profile 
#
