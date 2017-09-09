FROM python:3.6-alpine

RUN apk update
RUN apk add --virtual deps gcc python-dev linux-headers musl-dev postgresql-dev
RUN apk add --no-cache libpq

ADD . /code
WORKDIR /code
RUN pip install -e .
