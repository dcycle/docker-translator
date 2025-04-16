#!/bin/bash
# Tests
set -e
# docker run --rm -v $(pwd)/docker-resources:/app/code dcycle/python-lint:2 ./code
docker pull python:alpine
docker build -t local-translate-api-image .

! docker run --rm local-translate-api-image preflight.py
echo "[ok] preflight.py returns an error if no environment vars are set"

docker run --rm \
  -e MS_ENDPOINT="https://this has to start with https:// but otherwise can be anything" \
  -e MS_LOC="this can be anything to make preflight pass" \
  -e MS_KEY="this can be anything to make preflight pass" \
  -e MS_SIMULATE="true" \
  local-translate-api-image preflight.py
echo "[ok] preflight.py passes if environment vars are set"
