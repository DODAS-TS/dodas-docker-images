FROM mircot/htcondordask:v5

RUN pip3 install dask-remote-jobqueue==v0.4.8

RUN pip3 install jupyter-packaging
RUN git clone --branch custom_clusters https://github.com/DODAS-TS/dask-labextension.git \
    && cd dask-labextension \
    && python3 -m pip install .

COPY spawn.sh /.init/spawn.sh
RUN echo "source ~/htc.rc" >> ~/.bashrc
COPY kernel.json /usr/local/share/jupyter/kernels/python3/kernel.json
