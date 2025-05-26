"""Translate a file"""

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
    parser.add_argument('--source', required=True)
    # pylint: disable=R0801
    parser.add_argument('--destination', required=True)
    parser.add_argument('--source-lang', required=True)
    parser.add_argument('--dest-lang', required=True)
    parser.add_argument('--provider', required=True)
    parser.add_argument('--preprocessors', default="[]")
    parser.add_argument('--postprocessors', default="[]")

    args = parser.parse_args()

    with open(args.source, 'r', encoding='utf-8') as f:
        text = f.read()

    result = my_translate.translate({
      'provider': args.provider,
      'text': text,
      'from_lg': args.source_lang,
      'to': [args.dest_lang],
      'preprocessors': json.loads(args.preprocessors),
      'postprocessors': json.loads(args.postprocessors),
    })[0]['translations'][0]['text']

    with open(args.destination, 'w', encoding='utf-8') as out_f:
        out_f.write(result)

if __name__ == '__main__':
    main()
