ARG BASE_CONTAINER=dodasts/htcondor
FROM $BASE_CONTAINER

COPY condorconfig/* /etc/condor/
COPY config.d/* /etc/condor/config.d/

COPY dodas_bin/*  /usr/local/bin/

RUN chmod +x /usr/local/bin/dodasexe_pre.sh \
    && chmod +x /usr/local/bin/dodasexe.sh \
    && chmod +x /usr/local/bin/dodas.sh

RUN mkdir -p /etc/condor/certs \
    && cp /etc/condor/config.d/condor_mapfile /etc/condor/certs/condor_mapfile \
    && rm /etc/condor/config.d/condor_mapfile

WORKDIR /root

# Download validation script
RUN wget https://gitlab.cern.ch/CMSSI/CMSglideinWMSValidation/raw/master/singularity_validation.sh \
    && wget https://gitlab.cern.ch/CMSSI/CMSglideinWMSValidation/raw/master/singularity_wrapper.sh -O /usr/local/libexec/singularity_wrapper.sh

RUN   chmod +x /usr/local/libexec/singularity_wrapper.sh \
    && chmod 0755 /usr/local/libexec/singularity_wrapper.sh \
    && chown condor:condor /usr/local/libexec/singularity_wrapper.sh


ENTRYPOINT ["/usr/local/bin/dodas.sh"]