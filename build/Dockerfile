###############
# PYTHON BASE #
###############
FROM python:3.9-alpine as py-base

ARG DOCKER_UID

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN set -xe; \
    apk add --update --no-cache \
        openssl;

######################
# PYTHON DEVELOPMENT #
######################
FROM py-base as py-development

ARG DOCKER_UID

RUN set -xe; \
    apk add --update --no-cache \
        bash \
        bash-completion \
        build-base \
        openssl \
        libffi-dev; \
    apk add --no-cache --virtual .build-deps shadow; \
    mkdir -p /var/www/html; \
    useradd -u ${DOCKER_UID} www-data -d /var/www; \
    chown -R www-data:www-data /var/www; \
    apk del --no-network .build-deps; \
    pip install pipenv; \
    echo "export PS1=\"\\e[0;37m\\]\\u@\\e[4;31m\\]\\h\\e[0;37m\\] \\w \\e[0m\\]> \"" > /var/www/.bashrc;

ENV SHELL=/bin/bash

WORKDIR /var/www/html

USER www-data

##################
# JS BASE #
##################
FROM node:15-alpine as js-base

ARG DOCKER_UID

RUN set -xe; \
    apk add --update --no-cache \
        openssl;

##################
# JS DEVELOPMENT #
##################
FROM js-base as js-development

ARG DOCKER_UID

RUN set -xe; \
    apk add --update --no-cache \
        bash \
        bash-completion \
        build-base; \
    apk add --no-cache --virtual .build-deps shadow; \
    mkdir -p /var/www/html; \
    deluser --remove-home node; \
    useradd -u ${DOCKER_UID} www-data -d /var/www; \
    chown -R www-data:www-data /var/www; \
    apk del --no-network .build-deps; \
    echo "export PS1=\"\\e[0;37m\\]\\u@\\e[4;32m\\]\\h\\e[0;37m\\] \\w \\e[0m\\]> \"" > /var/www/.bashrc;

ENV SHELL=/bin/bash

WORKDIR /var/www/html

USER www-data

##################
# JS PRODUCTION #
##################
FROM js-base as js-production

WORKDIR /var/www/html

COPY ./front .

RUN set -xe; \
    npm ci; \
    npm run build;

#####################
# PYTHON PRODUCTION #
#####################
FROM py-base as py-dependencies

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN set -xe; \
    apk add --update --no-cache \
        build-base \
        openssl \
        libffi-dev;

# Install python dependencies in /.venv
COPY ./api/Pipfile* ./

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM py-base AS py-production

ENV USER_NAME=limited-user

# Copy virtual env from python-deps stage
COPY --from=py-dependencies /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Create a new user
RUN set -xe; \
    apk add --no-cache --virtual .build-deps shadow; \
    mkdir -p /var/www/html; \
    useradd $USER_NAME -d /var/www; \
    chown -R ${USER_NAME}:${USER_NAME} /var/www; \
    apk del --no-network .build-deps;

WORKDIR /var/www/html

USER $USER_NAME

COPY ./api ./
COPY --from=js-production /var/www/html/dist ./front/dist

EXPOSE 5000

CMD python serve.py
