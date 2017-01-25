# vim:set ft=dockerfile:
FROM debian:jessie
MAINTAINER andrii.gakhov@gmail.com

# BUILD EXAMPLE:
#    docker build -t gakhov/api.boilerplate .
# RUN EXAMPLE:
#    docker run --rm -ti -u api -w /api -e IN_DOCKER_CONTAINER=true -e API_ENV={environment} -e API_REDIS_SERVER="redis://localhost:6379/2" gakhov/api.boilerplate

ARG API_ENV
ARG API_VERSION=undefined

LABEL Description="This is API.BOILERPLATE image" Version=$API_VERSION

# Create user `api`
USER root
RUN useradd -ms /bin/bash api

USER root
RUN set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        apt-transport-https \
        build-essential \
        ca-certificates \
        make \
        python3-dev \
        python-virtualenv \
        software-properties-common \
        virtualenv \
        libffi-dev \
        wget \
    && rm -rf /var/lib/apt/lists/*

# Install local redis server
RUN set -x \
    && apt-get install -y --no-install-recommends \
        redis-server \
    && rm -rf /var/lib/apt/lists/*

# Make the "en_US.UTF-8" locale
RUN apt-get update \
    && apt-get install -y locales \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

# Create working directory
RUN rm -rf /api && mkdir /api
RUN chown -R api:api /api

USER api
COPY . /api
WORKDIR /api

RUN make clean \
    && make \
    && make install \
    && make all-tests

USER root

# Cleanup
RUN apt-get purge -y apt-transport-https\
    && rm -rf /var/lib/apt/lists/*

HEALTHCHECK --interval=30s --retries=3 \
    CMD curl -f http://localhost:5570/_health || exit 1

EXPOSE 5570
CMD ["bin/start_server"]
