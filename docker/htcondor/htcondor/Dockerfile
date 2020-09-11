FROM dodasts/tts-cache:v0.1.3-k8s-12 as TTS
FROM  htcondor/base:8.9.7-el7 as BASE

WORKDIR /etc/yum.repos.d

RUN yum install -y wget

RUN wget https://research.cs.wisc.edu/htcondor/yum/repo.d/htcondor-testing-rhel7.repo \
    && wget http://research.cs.wisc.edu/htcondor/yum/RPM-GPG-KEY-HTCondor \
    && rpm --import RPM-GPG-KEY-HTCondor \
    && yum --setopt=tsflags=nodocs -y update \
    && yum --setopt=tsflags=nodocs -y install \
        gcc \
        #gcc-c++ \
        #make \
        #openssh-clients \
        #openssh-server \
        python-devel \
        python-pip \
    && yum clean all 


FROM BASE as APP

# Root home
WORKDIR /root

# condor_collector
EXPOSE 9618
# condor_negotiator
EXPOSE 9614
# condor_ckpt_server
EXPOSE 5651-5654
# condor_ports
EXPOSE 1024-2048
# condor env default values
ENV CONDOR_DAEMON_LIST="COLLECTOR, MASTER, NEGOTIATOR, SCHEDD, STARTD"
ENV CONDOR_HOST="\$(FULL_HOSTNAME)"
ENV CCB_ADDRESS_STRING=""
ENV NETWORK_INTERFACE_STRING=""
ENV CONDOR_SCHEDD_SSH_PORT=31042
ENV TUNNEL_FROM="UNDEFINED"
ENV TUNNEL_TO="UNDEFINED"
ENV SEC_DAEMON_AUTHENTICATION_METHODS=CLAIMTOBE
ENV SEC_CLIENT_AUTHENTICATION_METHODS=CLAIMTOBE
ENV SEC_NEGOTIATOR_AUTHENTICATION_METHODS=CLAIMTOBE
ENV SEC_ADVERTISE_STARTD_AUTHENTICATION_METHODS=CLAIMTOBE
ENV NUM_SLOTS=1 
ENV NUM_SLOTS_TYPE_1=1
ENV SLOT_TYPE_1="cpus=1, mem=4096"
ENV FLOCK_FROM=""
ENV FLOCK_TO=""
ENV FLOCK_TO_COL_NEG=""
ENV HOST_ALLOW_FLOCK=""

RUN mkdir -p /opt/dodas/htc_config \
    && mkdir -p /opt/dodas/fs_remote_dir \
    && mkdir -p /opt/dodas/health_checks \
    && mkdir -p /etc/skel/.ssh
COPY condor.sh /opt/dodas/
COPY ./health_checks/check_condor_processes.py /opt/dodas/health_checks/
COPY ./health_checks/check_cvmfs_folders.py /opt/dodas/health_checks/
COPY ./health_checks/check_ssh_server.py /opt/dodas/health_checks/
COPY ./health_checks/check_condor_master_ip.sh /opt/dodas/health_checks/
COPY ./health_checks/check_condor_schedd_tunnel.sh /opt/dodas/health_checks/
COPY cache.py /opt/dodas/
COPY ./config/condor_config_schedd.template /opt/dodas/htc_config/
COPY ./config/condor_config_master.template /opt/dodas/htc_config/
COPY ./config/condor_config_wn.template /opt/dodas/htc_config/
COPY webapp /opt/dodas/htc_config/webapp
RUN mkdir -p /var/log/form/

RUN ln -s /opt/dodas/condor.sh /usr/local/sbin/dodas_condor \
    && ln -s /opt/dodas/health_checks/check_condor_processes.py /usr/local/sbin/dodas_check_condor_processes \
    && ln -s /opt/dodas/health_checks/check_cvmfs_folders.py /usr/local/sbin/dodas_check_cvmfs_folders \
    && ln -s /opt/dodas/health_checks/check_ssh_server.py /usr/local/sbin/dodas_check_ssh_server \
    && ln -s /opt/dodas/health_checks/check_condor_master_ip.sh /usr/local/sbin/dodas_check_condor_master_ip \
    && ln -s /opt/dodas/health_checks/check_condor_schedd_tunnel.sh /usr/local/sbin/dodas_check_condor_schedd_tunnel \
    && ln -s /opt/dodas/cache.py /usr/local/sbin/dodas_cache

# CentOS uname characteristics
RUN mv /bin/uname /bin/uname_old
COPY ./bin/uname /bin/

COPY --from=0 /usr/local/bin/tts-cache /usr/local/bin/tts-cache

RUN yum -y install epel-release httpd mod_wsgi mod_ssl net-tools vim python2-pip git
#RUN yum -y install https://repo.opensciencegrid.org/osg/3.4/osg-3.4-el7-release-latest.rpm 
COPY condor.repo /etc/yum.repos.d/condor.repo

RUN yum update -y && yum install -y condor-all &&  systemctl disable condor
#RUN yum install -y https://research.cs.wisc.edu/htcondor/yum/infn/rhel7/condor-all-8.9.7-0.502311.el7.x86_64.rpm
# || :
RUN yum install -y https://github.com/scitokens/scitokens/releases/download/v1.2.0/python2-scitokens-1.2.0-1.el7.noarch.rpm
RUN yum install -y https://research.cs.wisc.edu/htcondor/yum/infn/rhel7/python2-scitokens-credmon-0.6-0.2.el7.noarch.rpm

#RUN pip install --upgrade pip
RUN  pip install --upgrade pip \
    && pip install j2cli paramiko psutil kazoo requests flask Flask-WTF wtforms
#RUN pip install git+https://github.com/htcondor/scitokens-credmon

RUN pip install cffi==1.13.0 urltools

ENTRYPOINT ["/usr/local/sbin/dodas_condor"]

FROM APP AS TOKEN


RUN mkdir -p /var/lib/condor/credentials && \
    chgrp condor /var/lib/condor/credentials && \
    chmod 2770 /var/lib/condor/credentials

COPY httpd/ssl.conf /etc/httpd/conf.d/ssl.conf
RUN mkdir -p  /var/www/wsgi-scripts/scitokens-credmon/
COPY httpd/scitokens-credmon.wsgi /var/www/wsgi-scripts/scitokens-credmon/scitokens-credmon.wsgi
COPY httpd/scitokens_credmon.conf /etc/httpd/conf.d/scitokens_credmon.conf

RUN  systemctl disable condor

RUN wget https://research.cs.wisc.edu/htcondor/yum/infn/rhel7/ZKM-CUSTOM-00.tar.gz

RUN tar -xzvf ZKM-CUSTOM-00.tar.gz

RUN cp -r release_dir/bin/* /bin/

RUN cp -r release_dir/sbin/* /sbin/

#RUN mkdir /etc/init.d/network

RUN cp -r release_dir/etc/init.d/condor /etc/init.d/condor 

RUN cp -r release_dir/lib/* /lib/

RUN cp -r release_dir/lib64/* /lib64/

# TODO: fix user_info in OAUTH_MON.py

ENTRYPOINT ["/usr/local/sbin/dodas_condor"]