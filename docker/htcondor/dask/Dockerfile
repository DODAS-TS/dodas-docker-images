FROM htcondor/execute:8.9.9-el7

RUN python3 -m pip install -U pip setuptools

RUN pip3 install dask-remote-jobqueue==v0.4.14.dev0

# RUN pip3 install jupyter-packaging
# RUN git clone --branch custom_clusters https://github.com/DODAS-TS/dask-labextension.git \
#     && cd dask-labextension \
#     && python3 -m pip install .

# COPY spawn.sh /.init/spawn.sh
# RUN echo "source ~/htc.rc" >> ~/.bashrc
# COPY kernel.json /usr/local/share/jupyter/kernels/python3/kernel.json
