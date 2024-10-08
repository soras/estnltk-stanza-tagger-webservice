FROM continuumio/miniconda3

# NAURON_MODE is a build argument and an environment variable that determines whether the image contains a full API, a
# gateway API or a worker. Expected value is one of ["API", "GATEWAY", "WORKER"].

ARG NAURON_MODE="API"
ENV NAURON_MODE=$NAURON_MODE

# Configuring Conda environment
COPY environments/* ./
RUN if [ "$NAURON_MODE" = "GATEWAY" ]; then \
        conda env create -f environment.gateway.yml -n nauron; \
    elif [ "$NAURON_MODE" = "WORKER" ]; then \
        conda env create -f environment.worker.yml -n nauron; \
    else \
        conda env create -f environment.api.yml -n nauron; \
    fi; \
    rm environment*

WORKDIR /var/log/nauron
WORKDIR /stanza_syntax_tagger
VOLUME /stanza_syntax_tagger/stanza_resources

# Creating a mode-dependent entrypoint script
RUN if [ "$NAURON_MODE" = "WORKER" ]; then \
        echo "python stanza_tagger_worker.py" > run.sh; \
        echo "python ensemble_tagger_worker.py" > run.sh; \
    else \
        echo "gunicorn --config config/gunicorn.ini.py --log-config config/logging.ini app:app" > run.sh; \
    fi

COPY . .

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "nauron", "bash", "run.sh"]