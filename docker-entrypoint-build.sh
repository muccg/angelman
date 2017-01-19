#!/bin/bash

info () {
    printf "\r  [\033[00;34mINFO\033[0m] %s\n" "$1"
}

trap exit SIGHUP SIGINT SIGTERM
env | grep -iv PASS | sort

# prepare a tarball of build
if [ "$1" = 'releasetarball' ]; then
    echo "[Run] Preparing a release tarball"
    info "BUILD_VERSION ${BUILD_VERSION}"

    set -e
    cd /app
    rm -rf /app/*
    set -x
    git clone --depth=1 --branch="${GIT_BRANCH}" "${PROJECT_SOURCE}" .
    git rev-parse HEAD > .version

    # Note: Environment vars are used to control the behaviour of pip (use local devpi for instance)
    pip install --upgrade -r "${PROJECT_NAME}"/runtime-requirements.txt
    pip install -e "${PROJECT_NAME}"
    set +x

    # vars for creating release tarball
    ARTIFACTS="/env
               /app/docker-entrypoint.sh
               /app/uwsgi
               /app/${PROJECT_NAME}"
    TARBALL="/data/${PROJECT_NAME}-${BUILD_VERSION}.tar"
    # shellcheck disable=SC2037
    TAR_OPTS="--exclude-vcs
              --verify
              --checkpoint=1000
              --checkpoint-action=dot
              --create
              --preserve-permissions"
 
    info "ARTIFACTS ${ARTIFACTS}"
    info "TARBALL ${TARBALL}"
 
    # create tar from / so relative and absolute paths are identical
    # allows archive verification to work
    cd /
    set -x
    # shellcheck disable=SC2086
    rm -f "${TARBALL}" && tar ${TAR_OPTS} -f "${TARBALL}" ${ARTIFACTS}
    set +x
    info "$(ls -lath "${TARBALL}")"
    rm -f "${TARBALL}.gz" && gzip "${TARBALL}"
    info "$(ls -lath "${TARBALL}.gz")"
    exit 0
fi

echo "[RUN]: Builtin command not provided [releasetarball]"
echo "[RUN]: $*"

exec "$@"
