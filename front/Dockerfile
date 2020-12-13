FROM node:15.4-alpine

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
        jq;

ARG DOCKER_UID

RUN set -xe; \
    apk add --no-cache --virtual .build-deps shadow; \
    mkdir -p /var/www/html; \
    deluser --remove-home node; \
    useradd -u ${DOCKER_UID} www-data -d /var/www; \
    chown -R www-data:www-data /var/www; \
    apk del --no-network .build-deps;

WORKDIR /var/www/html

USER www-data
