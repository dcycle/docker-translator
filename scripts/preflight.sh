#!/bin/bash
# Tests a connection to Microsft Translation
set -e

if [ -z "$MS_ENDPOINT" ]; then
  echo "MS_ENDPOINT is not set. Please set it to your Microsoft Translator endpoint."
  exit 1
fi
if [ -z "$MS_LOC" ]; then
  echo "MS_LOC is not set. Please set it to your Microsoft Translator location."
  exit 1
fi
if [ -z "$MS_KEY" ]; then
  echo "MS_KEY is not set. Please set it to your Microsoft Translator key."
  exit 1
fi

docker run --rm \
  -e MS_ENDPOINT="$MS_ENDPOINT" \
  -e MS_LOC="$MS_LOC" \
  -e MS_KEY="$MS_KEY" \
  local-translator-api-image preflight.py
