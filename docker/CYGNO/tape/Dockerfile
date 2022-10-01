FROM gmazzitelli/cygno-tape:v1.0.1-cygno

WORKDIR /etc/yum.repos.d

RUN  wget https://repo.data.kit.edu/data-kit-edu-centos7.repo

RUN yum install -y \
    oidc-agent \
    && yum clean all 

WORKDIR /root
RUN sed -i 's/\/bin\/bin\//\/bin\//g' /usr/bin/oidc-agent-service
RUN wget https://raw.githubusercontent.com/gmazzitelli/dodas-docker-images/master/docker/CYGNO/tape/oicd-setup.sh
RUN wget https://raw.githubusercontent.com/gmazzitelli/dodas-docker-images/master/docker/CYGNO/tape/cygno_s32tape.sh
RUN wget https://raw.githubusercontent.com/gmazzitelli/dodas-docker-images/master/docker/CYGNO/tape/s32tape.py
RUN chmod a+x oicd-setup.sh cygno_s32tape.sh s32tape.py
