FROM python:3.10-slim

RUN mkdir /unittestingdash-sprinklr-main
WORKDIR /unittestingdash-sprinklr-main

COPY requirements.txt /
RUN pip install -r /requirements.txt

ENV ENVIRONMENT_FILE=".env"

COPY ./ ./
EXPOSE 8080

ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "index:server"]