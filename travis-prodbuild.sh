#!/bin/bash

set -e

#
# Production (deployable) build and tests
#

./develop.sh run-builder
./develop.sh build prod
./develop.sh aloe prod
#./develop.sh push prod
