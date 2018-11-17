#!/usr/bin/env bash

# get gid of docker socket file
if [ "$(uname)" == "Darwin" ]; then
    # SOCK_DOCKER_GID=`stat -f '%g' /var/run/docker.sock`
    # because of VM they mount docker.sock as root
    SOCK_DOCKER_GID=0
else
    SOCK_DOCKER_GID=`stat -c '%g' /var/run/docker.sock`
fi

docker build --build-arg SOCK_DOCKER_GID=$SOCK_DOCKER_GID -t isi/mint-jenkins .
