#!/bin/bash
# Tests a connection to Microsft Translation
set -e

docker run --rm \
  -e MS_ENDPOINT="$MS_ENDPOINT" \
  -e MS_LOC="$MS_LOC" \
  -e MS_KEY="$MS_KEY" \
  local-translate-api-image preflight.py
