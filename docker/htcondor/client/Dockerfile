FROM htcondor/submit:8.9.9-el7

copy htcondor_ca.crt /etc/pki/ca-trust/source/anchors/htcondor_ca.crt
copy condor_config.local /etc/condor/condor_config.local

RUN yum -y install https://github.com/indigo-dc/oidc-agent/releases/download/v4.0.2/oidc-agent-4.0.2-1.el7.x86_64.rpm

