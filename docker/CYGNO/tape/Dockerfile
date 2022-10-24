FROM ubuntu:22.04
RUN apt update -y && apt install -y python3 python3-pip oidc-agent git

RUN pip install git+https://github.com/DODAS-TS/boto3sts
RUN pip install 'https://github.com/CYGNUS-RD/middleware/blob/master/midas/midaslib.tar.gz?raw=true'
RUN pip install git+https://github.com/CYGNUS-RD/cygno.git

RUN ln -s /usr/bin/python3 /usr/bin/python
RUN mkdir /root/script
WORKDIR /root/script
