# Image name: dodasts/snj-base-jlabc
# Image name: dodasts/snj-base-jlabc-gpu -> based on tensorflow/tensorflow:2.7.0rc1-gpu (with ubuntu 20:04)
ARG BASE_IMAGE="dodasts/snj-base-lab"
FROM ${BASE_IMAGE}

COPY jupyter_lab_config.py /usr/local/share/dodasts/jupyter_configs/

RUN python3 -m pip install --no-cache-dir jupyterlab-link-share==0.2.1

RUN /bin/bash -c "jupyter lab build"

WORKDIR /jupyter-workspace

CMD ["jupyter", "lab", "--debug", \
    "--JupyterApp.config_file=/usr/local/share/dodasts/jupyter_configs/jupyter_lab_config.py", \
    "--ServerApp.keyfile=/usr/local/share/dodasts/certs/jupyter/hostcert.key", \
    "--ServerApp.certfile=/usr/local/share/dodasts/certs/jupyter/hostcert.pem", \
    "--MappingKernelManager.cull_idle_timeout=10800", \
    "--MappingKernelManager.cull_connected=True"]
