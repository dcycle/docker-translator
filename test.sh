#!/bin/bash
# Tests
set -e

mkdir -p ./do-not-commit

# See https://github.com/dcycle/docker-python-lint
echo ""
echo "To ignore a line, you can add this before the line"
echo "# pylint: disable=E0401"
echo ""
docker run --rm -v $(pwd)/docker-resources:/app/code dcycle/python-lint:2 ./code
docker pull python:alpine
docker build -t local-translator-api-image .

! docker run --rm local-translator-api-image preflight.py
echo "[ok] preflight.py returns an error if no environment vars are set"

docker run --rm \
  -e MS_ENDPOINT="https://this has to start with https:// but otherwise can be anything" \
  -e MS_LOC="this can be anything to make preflight pass" \
  -e MS_KEY="this can be anything to make preflight pass" \
  -e MS_SIMULATE="true" \
  local-translator-api-image preflight.py
echo "[ok] preflight.py passes if environment vars are set"

./scripts/translate-md.sh --source example01/test-file.md \
  --langkey this_is_the_language_key \
  --source-lang en \
  --dest-lang fr \
  --destination-folder do-not-commit \
  --provider simulate \
  --translate-key translation_info_key \
  --translate-message "Translated by @provider from @source using @repo on @date" \
  --do-not-translate-frontmatter '["title", "something", "whatever"]' \
  --do-not-translate-regex \
  --remove-span-translate-no

echo "[ok] translate-md.sh works with simulator"

rm -rf ./do-not-commit
