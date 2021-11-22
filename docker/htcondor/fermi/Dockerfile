FROM htcondor/execute:8.9.9-el7

RUN curl -k "https://crt.sh/?d=2475254782" -o /etc/pki/ca-trust/source/anchors/ca.crt
RUN update-ca-trust
ENV PATH="/cvmfs/fermi.local.repo/anaconda3/bin:${PATH}"
ENV HEADAS="/cvmfs/fermi.local.repo/ftools/x86_64-pc-linux-gnu-libc2.17"

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
