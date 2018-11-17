FROM jenkinsci/blueocean:1.8.3

ARG SOCK_DOCKER_GID

USER root
RUN apk --no-cache add shadow \
    && groupadd -f -g $SOCK_DOCKER_GID docker_group && usermod -aG $SOCK_DOCKER_GID jenkins

RUN apk --no-cache --allow-untrusted -X https://apkproxy.herokuapp.com/sgerrand/alpine-pkg-glibc add glibc glibc-bin \
    && curl -L "https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose

USER jenkins