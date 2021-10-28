# Image name: dodasts/snj-base-jlabc
# Image name: dodasts/snj-base-jlabc-gpu -> based on tensorflow/tensorflow:2.7.0rc1-gpu (with ubuntu 20:04)
ARG BASE_IMAGE="dodasts/snj-base-lab"
FROM ${BASE_IMAGE}

WORKDIR /usr/local/share/dodasts

RUN git clone https://github.com/DODAS-TS/jupyterlab-collaborative-util-extension.git \
    && cd jupyterlab-collaborative-util-extension \
    && jupyter labextension install

COPY jupyter_lab_config.py /usr/local/share/dodasts/jupyter_configs/

RUN /bin/bash -c "jupyter lab build"

CMD ["jupyter", "lab", "--debug", \
    "--JupyterApp.config_file=/usr/local/share/dodasts/jupyter_configs/jupyter_lab_config.py", \
    "--ServerApp.keyfile=/usr/local/share/dodasts/certs/jupyter/hostcert.key", \
    "--ServerApp.certfile=/usr/local/share/dodasts/certs/jupyter/hostcert.pem", \
    "--MappingKernelManager.cull_idle_timeout=10800", \
    "--MappingKernelManager.cull_connected=True"]
