"""Translate text"""

import json
# pylint: disable=E0401
import argparse
# pylint: disable=E0401
import my_translate

def main():
    """
    Main function to translate a content language to another.
    """
    parser = argparse.ArgumentParser(description='Translate content.')
    parser.add_argument('--text', required=True)
    parser.add_argument('--source-lang', required=True)
    parser.add_argument('--dest-lang', required=True)
    parser.add_argument('--provider', required=True)
    parser.add_argument('--preprocessors', default="[]")
    parser.add_argument('--postprocessors', default="[]")

    args = parser.parse_args()

    print(my_translate.translate({
      'provider': args.provider,
      'text': args.text,
      'from_lg': args.source_lang,
      'to': [args.dest_lang],
      'preprocessors': json.loads(args.preprocessors),
      'postprocessors': json.loads(args.postprocessors),
    })[0]['translations'][0]['text'])

if __name__ == '__main__':
    main()
