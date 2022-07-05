# Image name: dodasts/snj-base-jlabc
# Image name: dodasts/snj-base-jlabc-gpu -> based on tensorflow/tensorflow:2.7.0rc1-gpu (with ubuntu 20:04)
ARG BASE_IMAGE="dodasts/snj-base-lab"
FROM ${BASE_IMAGE}

COPY jupyter_lab_config.py /usr/local/share/dodasts/jupyter_configs/

RUN python3 -m pip install --no-cache-dir jupyterlab-link-share==0.2.1

## Apply patch for fixing SSL/TLS handshakes (Renegotiation) 
## over an existing / already established SSL/TLS connection 
## CVE-2011-1473, CVE-2011-5094
COPY netutil.py.patch /tmp/
RUN patch -b /usr/local/lib/python3.8/dist-packages/tornado/netutil.py /tmp/netutil.py.patch

# Build jupyter lab stuff
RUN /bin/bash -c "jupyter lab build --dev-build=False --minimize=True"

WORKDIR /jupyter-workspace

CMD ["tini", "-s", "--", "jupyter", "lab", "--debug", \
    "--JupyterApp.config_file=/usr/local/share/dodasts/jupyter_configs/jupyter_lab_config.py", \
    "--ServerApp.keyfile=/usr/local/share/dodasts/certs/jupyter/hostcert.key", \
    "--ServerApp.certfile=/usr/local/share/dodasts/certs/jupyter/hostcert.pem", \
    "--MappingKernelManager.cull_idle_timeout=10800", \
    "--MappingKernelManager.cull_connected=True"]
