# FROM dodasts/cygno-lab:<latest release> -> for example:
FROM dodasts/cygno-lab:v1.0.16-cygno

# Testetd updadete implemented in v1.0.16-cygno
# RUN pip3 install 'https://github.com/CYGNUS-RD/middleware/blob/master/midas/midaslib.tar.gz?raw=true'
# RUN pip3 install tensorflow
# RUN pip3 install keras
# RUN pip3 install opencv-python
RUN ln -nfs /usr/bin/python2 /usr/bin/python

# just alwas run last update on CYGNO LIB
RUN pip3 install --no-cache-dir -U git+https://github.com/CYGNUS-RD/cygno.git

# Install Cron Centos 7
#RUN yum install -y cronie && yum clean all

#RUN crontab -l | { cat; echo "* * * * * /bin/rsync -a --delete /jupyter-workspace/private/ /jupyter-workspace/cloud-storage/mazzitel/private 2>&1"; } | crontab -

