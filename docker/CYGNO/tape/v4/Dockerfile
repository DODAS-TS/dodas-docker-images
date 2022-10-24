FROM gmazzitelli/cygno-tape:v1.0.1-cygno

WORKDIR /etc/yum.repos.d

RUN  wget https://repo.data.kit.edu/data-kit-edu-centos7.repo

RUN yum install -y \
    oidc-agent \
    && yum clean all 

RUN sed -i 's/\/bin\/bin\//\/bin\//g' /usr/bin/oidc-agent-service

RUN yum install -y git \
	python3 \
	python-pip

RUN pip3 install --upgrade pip
RUN pip3 install git+https://github.com/DODAS-TS/boto3sts
RUN pip3 install git+https://github.com/CYGNUS-RD/cygno.git
RUN pip2 install numpy==1.16.6

#RUN wget http://download-ib01.fedoraproject.org/pub/epel/7/aarch64/
#RUN yum install -y gfal2-util gfal2-all

RUN mkdir /root/script
WORKDIR /root/script

# RUN wget https://raw.githubusercontent.com/gmazzitelli/dodas-docker-images/master/docker/CYGNO/tape/oicd-setup.sh
# RUN wget https://raw.githubusercontent.com/gmazzitelli/dodas-docker-images/master/docker/CYGNO/tape/cygno_s32tape.sh
# RUN wget https://raw.githubusercontent.com/gmazzitelli/dodas-docker-images/master/docker/CYGNO/tape/s32tape.py
# RUN chmod a+x oicd-setup.sh cygno_s32tape.sh s32tape.py
