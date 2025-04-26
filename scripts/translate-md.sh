#!/bin/bash

set -e

# Default values
LANGKEY="lang"
DEST_FOLDER=""
PROVIDER="microsoft"
TRANSLATE_KEY="translation"
TRANSLATE_MESSAGE="Translated by @Provider from @source using @repo on @Date"
DO_NOT_TRANSLATE_KEYS=()

# Helper to show usage
usage() {
  echo "Usage: $0 --source <file> --source-lang <lang> --dest-lang <lang> [options]"
  echo
  echo "Options:"
  echo "  --source                      Source markdown file (required)"
  echo "  --langkey                    Frontmatter language key (default: lang)"
  echo "  --source-lang                Source language (required)"
  echo "  --dest-lang                  Destination language (required)"
  echo "  --destination-folder         Output folder (default: same as source)"
  echo "  --provider                   Translation provider (default: microsoft)"
  echo "  --translate-key              Frontmatter key for translation info (default: translation)"
  echo "  --translate-message          Message template (default: 'Translated by @Provider from @source using @repo on @Date')"
  echo "  --do-not-translate-frontmatter <key>  Frontmatter key to exclude from translation (can be repeated)"
  exit 1
}

# Parse arguments
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
    --do-not-translate-frontmatter)
      DO_NOT_TRANSLATE_KEYS+=("$2")
      shift 2 ;;
    *)
      echo "Unknown option: $1"
      usage ;;
  esac
done

# Check required arguments
[[ -z "$SOURCE" || -z "$SOURCE_LANG" || -z "$DEST_LANG" ]] && usage

# Determine destination folder
if [[ -z "$DEST_FOLDER" ]]; then
  DEST_FOLDER=$(dirname "$SOURCE")
fi

# Create destination folder if it doesn't exist
mkdir -p "$DEST_FOLDER"

# Destination file
BASENAME=$(basename "$SOURCE" .md)
DEST_FILE="$DEST_FOLDER/${BASENAME}.${DEST_LANG}.md"

docker pull python:alpine
# docker build -t local-translate-api-image .

mkdir -p $(pwd)/do-not-commit

docker build -t local-translate-api-image .

docker run \
  -v $(pwd)/example01:/app/example01 \
  -v $(pwd)/docker-resources:/app \
  -v $(pwd)/do-not-commit:/app/do-not-commit \
  local-translate-api-image \
  /app/translate_markdown.py \
  --source "/app/$SOURCE" \
  --source-lang "$SOURCE_LANG" \
  --dest-lang "$DEST_LANG" \
  --provider "$PROVIDER" \
  --langkey "$LANGKEY" \
  --translate-key "$TRANSLATE_KEY" \
  --translate-message "$TRANSLATE_MESSAGE" \
  $(for key in "${DO_NOT_TRANSLATE_KEYS[@]}"; do echo "--do-not-translate-frontmatter $key"; done)

