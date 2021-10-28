# Image name: dodasts/ml-infn-lab
FROM dodasts/snj-base-lab-gpu

# Install system packages
RUN DEBIAN_FRONTEND=noninteractive apt install -y subversion graphviz libgl1 \
    build-essential libargon2-0-dev libffi-dev libpixman-1-dev libcairo2-dev libpangox-1.0-dev libjpeg-dev \
    libczmq-dev pandoc texlive-xetex texlive-fonts-recommended texlive-base \
    && apt clean

# Install python packages
RUN python3 -m pip install --no-cache-dir uproot keras matplotlib \
    sklearn torch pydot graphviz gwdama scikit-image opencv-python pandoc