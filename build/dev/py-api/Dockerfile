FROM python:3.9-alpine

RUN set -xe; \
    apk add --update --no-cache \
        bash \
        bash-completion \
        gcc \
        libc-dev \
        curl \
        openssl \
        git \
        make \
        grep \
        jq \
        libffi-dev;

RUN pip install pipenv

ARG DOCKER_UID
RUN set -xe; \
    apk add --no-cache --virtual .build-deps shadow; \
    mkdir -p /var/www/html; \
    useradd -u ${DOCKER_UID} www-data -d /var/www; \
    chown -R www-data:www-data /var/www; \
    apk del --no-network .build-deps;

COPY --chown=www-data:www-data .bashrc /var/www/.bashrc

USER www-data

WORKDIR /var/www/html
