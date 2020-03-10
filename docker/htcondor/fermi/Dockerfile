ARG BASE_CONTAINER=dodasts/htcondor
FROM $BASE_CONTAINER

ENV CONDAPFX="/cvmfs/fermi.local.repo/anaconda3"
ENV CONDABIN="${CONDAPFX}/bin/conda"

RUN yum install -y sqlite-devel \
  autoconf \
  automake \
  bzip2-devel \
  emacs \
  gcc \
  gcc-c++ \
  gcc-gfortran \
  git \
  libpng-devel \
  libSM-devel \
  libX11-devel \
  libXdmcp-devel \
  libXext-devel \
  libXft-devel \
  libXpm-devel \
  libXrender-devel \
  libXt-devel \
  make \
  mesa-libGL-devel \
  ncurses-devel \
  openssl-devel \
  patch \
  perl \
  perl-ExtUtils-MakeMaker \
  readline-devel \
  sqlite-devel \
  sudo \
  tar \
  vim \
  wget \
  which \
  zlib-devel && \
yum clean all && \
rm -rf /var/cache/yum

COPY condor.sh /opt/dodas/

RUN rm /usr/local/sbin/dodas_condor && ln -s /opt/dodas/condor.sh /usr/local/sbin/dodas_condor

ENV PATH="/cvmfs/fermi.local.repo/anaconda3/bin:${PATH}"
ENV HEADAS="/cvmfs/fermi.local.repo/ftools/x86_64-pc-linux-gnu-libc2.17"

ENTRYPOINT ["/usr/local/sbin/dodas_condor"]