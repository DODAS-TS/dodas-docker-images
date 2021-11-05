# Image name: dodasts/ml-infn-jlabc
FROM dodasts/snj-base-jlabc-gpu

# Install system packages
RUN DEBIAN_FRONTEND=noninteractive apt install -y subversion graphviz libgl1 \
    build-essential libargon2-0-dev libffi-dev libpixman-1-dev libcairo2-dev libpangox-1.0-dev libjpeg-dev \
    libczmq-dev pandoc texlive-xetex texlive-fonts-recommended texlive-base \
    && apt clean

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
    torch==1.10.0 \
    uproot==4.1.7