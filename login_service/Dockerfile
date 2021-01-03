FROM python:3.7.9-stretch

ENV ENVIRONMENT = "dev"
ENV FROM_EMAIL = ""
ENV FROM_PASSWORD = ""

ADD . /code

WORKDIR /code
COPY ./ /code

RUN pip install -r requirements.txt
