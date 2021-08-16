FROM mircot/htcondordask:v5

RUN pip3 install dask-remote-jobqueue==v0.3.6

COPY labextension.yaml /usr/local/lib/python3.6/site-packages/dask_labextension/labextension.yaml
COPY spawn.sh /.init/spawn.sh
RUN echo "source ~/htc.rc" >> ~/.bashrc
COPY kernel.json /usr/local/share/jupyter/kernels/python3/kernel.json
