#!/bin/bash

set -e

# Default values
LANGKEY="lang"
DEST_FOLDER=""
PROVIDER="microsoft"
TRANSLATE_KEY="translation"
TRANSLATE_MESSAGE="Translated by @Provider from @source using @repo on @Date"
DO_NOT_TRANSLATE_KEYS=[]
REGEX_PROC="False"
REMOVE_SPAN="False"
FORCE_IF_SAME_HASH="False"

# Usage function
usage() {
  echo "Usage: $0 --source <file> --source-lang <lang> --dest-lang <lang> [options]"
  echo
  echo "Options:"
  echo "  --source                      Source markdown file (required)"
  echo "  --langkey                     Frontmatter language key (default: lang)"
  echo "  --source-lang                 Source language (required)"
  echo "  --dest-lang                   Destination language (required)"
  echo "  --destination-folder          Output folder (default: same as source)"
  echo "  --provider                    Translation provider (default: microsoft)"
  echo "  --translate-key               Frontmatter key for translation info"
  echo "  --translate-message           Translation message template"
  echo "  --do-not-translate-frontmatter Keys to exclude"
  echo "  --do-not-translate-regex      Enable regex exclusion"
  echo "  --remove-span-translate-no    Remove <span translate='no'>"
  echo "  --force-if-same-hash          The translation should take place even if the hash is the same."
  exit 1
}

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --source) SOURCE="$2"; shift 2 ;;
    --langkey) LANGKEY="$2"; shift 2 ;;
    --source-lang) SOURCE_LANG="$2"; shift 2 ;;
    --dest-lang) DEST_LANG="$2"; shift 2 ;;
    --destination-folder) DEST_FOLDER="$2"; shift 2 ;;
    --provider) PROVIDER="$2"; shift 2 ;;
    --translate-key) TRANSLATE_KEY="$2"; shift 2 ;;
    --translate-message) TRANSLATE_MESSAGE="$2"; shift 2 ;;
    --do-not-translate-frontmatter) DO_NOT_TRANSLATE_KEYS=("$2"); shift 2 ;;
    --do-not-translate-regex) REGEX_PROC="True"; shift ;;
    --remove-span-translate-no) REMOVE_SPAN="True"; shift ;;
    --force-if-same-hash) FORCE_IF_SAME_HASH="True"; shift ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
done

# Required args check
[[ -z "$SOURCE" || -z "$SOURCE_LANG" || -z "$DEST_LANG" ]] && usage

# Set destination folder
if [[ -z "$DEST_FOLDER" ]]; then
  DEST_FOLDER=$(dirname "$SOURCE")
fi

mkdir -p "$DEST_FOLDER"

# Prepare output path
BASENAME=$(basename "$SOURCE" .md)
DEST_FILE="$DEST_FOLDER/${BASENAME}.${DEST_LANG}.md"

# Pull and build Docker
docker pull python:alpine
docker build -t local-translator-api-image .

mkdir -p $(pwd)/do-not-commit

# Prepare optional flags
[[ "$REGEX_PROC" == "True" ]] && DO_REGEX_FLAG="--do-not-translate-regex"
[[ "$REMOVE_SPAN" == "True" ]] && REMOVE_SPAN_FLAG="--remove-span-translate-no"
[[ "$FORCE_IF_SAME_HASH" == "True" ]] && FORCE_IF_SAME_HASH_FLAG="--force-if-same-hash"

# Run Docker translation
docker run \
  -e MS_ENDPOINT="$MS_ENDPOINT" \
  -e MS_LOC="$MS_LOC" \
  -e MS_KEY="$MS_KEY" \
  -v "$(pwd)/example01:/app/example01" \
  -v "$(pwd)/docker-resources:/app" \
  -v "$(pwd)/do-not-commit:/app/do-not-commit" \
  local-translator-api-image \
  /app/translate_markdown.py \
  --source "/app/$SOURCE" \
  --source-lang "$SOURCE_LANG" \
  --destination "/app/$DEST_FILE" \
  --dest-lang "$DEST_LANG" \
  --provider "$PROVIDER" \
  --langkey "$LANGKEY" \
  --translate-key "$TRANSLATE_KEY" \
  --translate-message "$TRANSLATE_MESSAGE" \
  --do-not-translate-frontmatter "$DO_NOT_TRANSLATE_KEYS" \
  $DNT_FRONTMATTER \
  $DO_REGEX_FLAG \
  $REMOVE_SPAN_FLAG \
  $FORCE_IF_SAME_HASH_FLAG
