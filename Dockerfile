FROM python:3.9

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
        gcc \
        g++ \
        libffi-dev \
        musl-dev

ENV PYTHONIOENCODING=utf-8
ENV MKL_NUM_THREADS=16
WORKDIR /app

RUN adduser --disabled-password --gecos "app" app && \
    chown -R app:app /app
USER app

ENV PATH="/home/app/.local/bin:${PATH}"

COPY --chown=app:app requirements.txt .
RUN pip install --user -r requirements.txt && \
    rm requirements.txt

RUN wget https://s3.hpc.ut.ee/estnltk/estnltk_resources/stanza_syntax_2023-01-21.zip && \
    unzip stanza_syntax_2023-01-21.zip -d stanza_resources && \
    mv -f stanza_resources/stanza_syntax/models_2023-01-21/* stanza_resources/ && \
    rm -r stanza_syntax_2023-01-21.zip stanza_resources/stanza_syntax


COPY --chown=app:app . .

EXPOSE 8000

ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--proxy-headers"]