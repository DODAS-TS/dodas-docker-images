FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y wget lsb-release fuse
RUN wget  https://ecsft.cern.ch/dist/cvmfs/cvmfs-release/cvmfs-release-latest_all.deb
RUN dpkg -i cvmfs-release-latest_all.deb 
RUN rm -f cvmfs-release-latest_all.deb
RUN apt-get update
RUN apt-get install -y cvmfs cvmfs-server cvmfs-config-default
RUN apt-get autoremove -y && apt-get clean

#RUN cvmfs_server mkfs test
RUN echo "user_allow_other" >> /etc/fuse.conf \
    && echo -e "\nCVMFS_HTTP_PROXY=DIRECT\n" >> /etc/cvmfs/default.conf

COPY scripts/entrypoint.sh /root/entrypoint.sh

RUN chmod +x /root/entrypoint.sh

ENTRYPOINT [ "/root/entrypoint.sh" ]
