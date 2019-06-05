############################################################
# Dockerfile to run a Django-based web application
# Development environment
############################################################

# Set the base image to use to Ubuntu
FROM python:3.7-alpine

# Set the file maintainer
MAINTAINER Tan Nguyen

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /src/app

# Copy project
COPY . /src/app

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps

# Install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile /usr/src/app/Pipfile
RUN pipenv install --skip-lock --system --dev

# run docker-entrypoint.sh
ENTRYPOINT ["/src/app/docker-entrypoint.sh"]

