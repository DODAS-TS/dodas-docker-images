# Image name: dodasts/snj-base-lab-persistence
ARG BASE_IMAGE="dodasts/snj-base-lab"
FROM ${BASE_IMAGE}

ARG JUPYTER_ROOT=/jupyter-workspace

COPY post_script.sh /usr/local/share/dodasts/script/
RUN chmod +x /usr/local/share/dodasts/script/post_script.sh

# Link folders
RUN mkdir -p ${JUPYTER_ROOT} \
    && ln -s /s3 ${JUPYTER_ROOT}/cloud-storage \
    && ln -s /shared ${JUPYTER_ROOT}/shared \
    && ln -s /private ${JUPYTER_ROOT}/private

WORKDIR ${JUPYTER_ROOT}
