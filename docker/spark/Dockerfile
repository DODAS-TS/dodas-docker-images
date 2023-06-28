
FROM dodasts/spark:v3.0.1-patch1

WORKDIR /home/$NB_USER/SWAN_projects
RUN mkdir -p .init
RUN wget https://github.com/DODAS-TS/sts-wire/releases/download/v2.1.2/sts-wire_linux -O ./.init/sts-wire && chmod +x ./.init/sts-wire
COPY ./spawn.sh ./.init/spawn.sh
RUN sudo chown -R $NB_USER .init

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
