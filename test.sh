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

docker run --rm local-translator-api-image \
  processor_md_code_test.py
docker run --rm local-translator-api-image \
  processor_simulate_test.py
docker run --rm local-translator-api-image \
  processor_translate_frontmatter_test.py

! docker run --rm local-translator-api-image preflight.py
echo "[ok] preflight.py returns an error if no environment vars are set"

docker run --rm \
  -e MS_ENDPOINT="https://this has to start with https:// but otherwise can be anything" \
  -e MS_LOC="this can be anything to make preflight pass" \
  -e MS_KEY="this can be anything to make preflight pass" \
  -e MS_SIMULATE="true" \
  local-translator-api-image preflight.py
echo "[ok] preflight.py passes if environment vars are set"

# verify double quotes wrapping in frontformatter
rm -rf do-not-commit

./scripts/translate-md.sh \
  --source example01/test-file.md \
  --langkey this_is_the_language_key \
  --source-lang en \
  --dest-lang fr \
  --destination-folder do-not-commit \
  --provider simulate \
  --translate-key translation_info_key \
  --translate-message "Translated by @provider from @source using @repo on @date" \
  --do-not-translate-frontmatter-double-quote \
  --do-not-translate-frontmatter '["title", "something", "whatever"]' \
  --do-not-translate-regex \
  --remove-span-translate-no \
  && echo "Done"

# create translation again using --force-if-same-hash
./scripts/translate-md.sh --source example01/test-file.md \
  --langkey this_is_the_language_key \
  --source-lang en \
  --dest-lang fr \
  --destination-folder do-not-commit \
  --provider simulate \
  --translate-key translation_info_key \
  --translate-message "Translated by @provider from @source using @repo on @date" \
  --do-not-translate-frontmatter-double-quote \
  --do-not-translate-frontmatter '["title", "something", "whatever"]' \
  --do-not-translate-regex \
  --remove-span-translate-no \
  --force-if-same-hash \
  && echo "Done"

# throw error hash if same hash present
./scripts/translate-md.sh --source example01/test-file.md \
  --langkey this_is_the_language_key \
  --source-lang en \
  --dest-lang fr \
  --destination-folder do-not-commit \
  --provider simulate \
  --translate-key translation_info_key \
  --translate-message "Translated by @provider from @source using @repo on @date" \
  --do-not-translate-frontmatter-double-quote \
  --do-not-translate-frontmatter '["title", "something", "whatever"]' \
  --do-not-translate-regex \
  --remove-span-translate-no \
  && echo "Done"

# create translation again using --force-if-same-hash
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
  --remove-span-translate-no \
  --force-if-same-hash \
  && echo "Done"

./scripts/translate-md.sh --source example01/test-file.md \
  --langkey this_is_the_language_key \
  --source-lang en \
  --dest-lang fr \
  --destination-folder do-not-commit \
  --provider simulate \
  --translate-key translation_info_key \
  --translate-message "Translated by @provider from @source using @repo on @date" \
  --do-not-translate-frontmatter '["title", "something", "whatever"]' \
  --do-not-translate-frontmatter-double-quote \
  --do-not-translate-regex \
  --remove-span-translate-no \
  --force-if-same-hash \
  && echo "Done"

echo "[ok] translate-md.sh works with simulator"

cat ./do-not-commit/test-file.fr.md

rm -rf ./do-not-commit

docker run --rm \
  local-translator-api-image \
  translate.py \
  --text "La liberté commence ou l'ignorance finit." \
  --source-lang fr \
  --dest-lang en \
  --provider simulate

docker run --rm \
  local-translator-api-image \
  translate.py \
  --text 'I met her on the ship <span translate="no">The Queen of Egypt</span>.' \
  --source-lang en \
  --dest-lang fr \
  --provider simulate \
  --postprocessors '[{"name": "remove-span-translate-no-simple", "args": {}}]'

rm -rf ./do-not-commit
mkdir -p ./do-not-commit

docker run --rm \
  -v "$(pwd)":/data \
  local-translator-api-image \
  translate_file.py \
  --source /data/example01/file-file01.txt \
  --destination /data/do-not-commit/file-file01.es.txt \
  --source-lang en \
  --dest-lang es \
  --provider simulate

cat ./do-not-commit/file-file01.es.txt

docker run --rm \
  -e DEBUG="1" \
  -e MS_ENDPOINT="$MS_ENDPOINT" \
  -e MS_KEY="$MS_KEY" \
  -e MS_LOC="$MS_LOC" \
  -v "$(pwd)":/data \
  local-translator-api-image \
  translate_markdown.py \
  --source /data/example01/simple-frontmatter.md \
  --destination /data/do-not-commit/simple-frontmatter.fr.md \
  --source-lang en \
  --dest-lang fr \
  --provider simulate \
  --preprocessors '[{"name": "translate-frontmatter", "args": {}}]' \
  --postprocessors '[{"name": "remove-span-translate-no", "args": {}}]' \
  && echo "Done"

cat ./do-not-commit/simple-frontmatter.fr.md
rm ./do-not-commit/simple-frontmatter.fr.md

docker run --rm \
  -e MS_ENDPOINT="$MS_ENDPOINT" \
  -e MS_KEY="$MS_KEY" \
  -e MS_LOC="$MS_LOC" \
  -v "$(pwd)":/data \
  local-translator-api-image \
  translate_markdown.py \
  --source /data/example01/simple-frontmatter.md \
  --destination /data/do-not-commit/simple-frontmatter.fr.md \
  --source-lang en \
  --dest-lang fr \
  --provider simulate \
  --preprocessors '[{"name": "translate-frontmatter", "args": {"translate": ["title"]}}]' \
  --postprocessors '[{"name": "remove-span-translate-no", "args": {}}]'

cat ./do-not-commit/simple-frontmatter.fr.md

docker run --rm \
  -e MS_ENDPOINT="$MS_ENDPOINT" \
  -e MS_KEY="$MS_KEY" \
  -e MS_LOC="$MS_LOC" \
  -v "$(pwd)":/data \
  local-translator-api-image \
  translate_markdown.py \
  --source /data/example01/code.md \
  --destination /data/do-not-commit/code.fr.md \
  --source-lang en \
  --dest-lang fr \
  --provider simulate \
  --preprocessors '[{"name": "translate-frontmatter", "args": {"translate": ["title"]}},{"name": "md-code", "args": {}}]' \
  --postprocessors '[{"name": "remove-span-translate-no", "args": {}}]'

cat ./do-not-commit/code.fr.md

echo ""
echo "[ok] All tests passed!"
echo ""
