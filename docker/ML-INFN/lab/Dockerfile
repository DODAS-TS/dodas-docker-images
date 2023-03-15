# Image name: dodasts/ml-infn-lab
FROM dodasts/snj-base-lab-gpu:v1.1.1-snj

# Install system packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    subversion=1.13.0-3ubuntu0.2 graphviz=2.42.2-3build2 libgl1=1.3.2-1~ubuntu0.20.04.2 \
    build-essential=12.8ubuntu1.1 libargon2-dev=0~20171227-0.2 libffi-dev=3.3-4 libpixman-1-dev=0.38.4-0ubuntu2.1 \
    libcairo2-dev=1.16.0-4ubuntu1 libpangox-1.0-dev=0.0.2-5ubuntu1 libjpeg-dev=8c-2ubuntu8 libczmq-dev=4.2.0-2 \
    pandoc=2.5-3build2 texlive-xetex=2019.20200218-1 texlive-fonts-recommended=2019.20200218-1 texlive-base=2019.20200218-1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install python packages
RUN python3 -m pip install --no-cache-dir \
    graphviz==0.17 \
    gwdama==0.5.3 \
    keras==2.7.0 \
    lalsuite==7.0 \
    matplotlib==3.4.3 \
    opencv-python==4.5.4.58 \
    pandoc==1.1.0 \
    pydot==1.4.2 \
    scikit-image==0.18.3 \
    scikit-learn==1.0.1 \
    seaborn==0.11.2 \
    torch==1.10.0 \
    uproot==4.1.7
