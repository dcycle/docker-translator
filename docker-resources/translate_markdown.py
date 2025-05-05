"""All translate markdown code"""

# pylint: disable=E0401
import argparse
# pylint: disable=E0401
import hashlib
# pylint: disable=E0401
from datetime import datetime
# pylint: disable=E0401
import os
# pylint: disable=E0401
import json
# pylint: disable=E0401
import my_translate
# pylint: disable=E0401
import utilities


def generate_hash(content):
    """
    Generate an MD5 hash from a given string.

    This function takes a text string (such as the contents of a README file),
    encodes it as UTF-8, and returns its MD5 hash as a hexadecimal string.

    Args:
        content (str): The input string to hash.

    Returns:
        str: The hexadecimal MD5 hash of the input.
    """
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def replace_message_placeholders(message, args):
    """
    Replace placeholders in a message template with actual values.

    This function takes a message template string and an argument object (typically
    parsed via argparse), and substitutes predefined placeholders in the message with:
      - The translation provider (`@Provider`)
      - The source language code (`@source`)
      - The repository URL (`@repo`)
      - The current date in ISO format (`@Date`, e.g., 2025-04-27)

    Args:
        message (str): The message template containing placeholders.
        args (argparse.Namespace): The parsed arguments containing at least
                                   `provider` and `source_lang` attributes.

    Returns:
        str: The message with all placeholders replaced by their corresponding values.
    """
    replacements = {
        '@provider': args.provider,
        '@source': args.source_lang,
        '@repo': 'http://github.com/dcycle/docker-translator',
        '@date': datetime.now().isoformat()[:10]  # YYYY-MM-DD
    }
    for placeholder, value in replacements.items():
        message = message.replace(placeholder, value)
    return f'"{message}"'

def check_existing_translation(dest_file, source_hash, args):
    """
    Check if the destination file already contains a translation of the current source content.

    This function reads the frontmatter of an existing translated markdown file and compares
    its stored hash against the provided `source_hash`. If the hashes match, it means the content
    has not changed since the last translation, so re-translation is skipped.

    Args:
        dest_file (str): Path to the destination markdown file.
        source_hash (str): MD5 hash of the current source content.
        args (argparse.Namespace): Parsed arguments including `source`, and `translate_key`
                                   used to locate the hash in the destination's frontmatter.

    Returns:
        bool: True if the existing translation matches the source content (no need to re-translate),
              False otherwise.
    """
    if not os.path.exists(dest_file):
        return False

    with open(dest_file, 'r', encoding='utf-8') as f:
        content = f.read()
        frontmatter = utilities.extract_frontmatter(content)
        # First, check if the value under translate_key is a dictionary containing a hash
        value = frontmatter.get(args.translate_key)
        if isinstance(value, dict) and value.get('hash') == source_hash:
            print(f"Did not translate because source hash of {args.source}, {source_hash}, "
                  f"is the same as the source hash key in the existing destination file")
            return True
    return False

def extract_and_write_translation(result, dest_file, args, source_hash):
    """Extract translation and write to file with updated frontmatter"""
    translated_text = result[0]['translations'][0]['text']

    # Prepare translation metadata
    translation_metadata = {
        'hash': source_hash,
        'message': replace_message_placeholders(
            args.translate_message, args
        )
    }

    # Get existing frontmatter (if any)
    existing_frontmatter = utilities.extract_frontmatter(translated_text)
    if existing_frontmatter is None:
        existing_frontmatter = {}

    # Prepare all frontmatter updates
    updates = {
      args.translate_key: translation_metadata
    }

    # Update the content
    final_content = utilities.update_frontmatter(translated_text, updates)

    # Write the file
    with open(dest_file, 'w', encoding='utf-8') as out_f:
        out_f.write(final_content)

    print(f"Translation saved to {dest_file}")

def main():
    """
    Main function to translate a markdown file from one language to another.

    This function reads a source markdown file, checks whether a translation already exists,
    applies various preprocessors and postprocessors based on the input arguments, and
    invokes a translation service to perform the translation. The translated content is
    then saved to the destination file.

    The function supports the following features based on input arguments:
    - Skipping translation of specific frontmatter keys.
    - Excluding lines matching a regex pattern from translation.
    - Removing <span translate='no'> tags from the content.

    Args:
        None: The arguments are parsed from the command line via argparse.

    Returns:
        None: This function doesn't return anything, but it performs file operations
              and prints out translation results to the console.
    """
    parser = argparse.ArgumentParser(description='Translate markdown content.')
    parser.add_argument('--source', required=True)
    parser.add_argument('--source-lang', required=True)
    # Add the destination-folder argument
    parser.add_argument('--destination', default=None)
    parser.add_argument('--dest-lang', required=True)
    parser.add_argument('--provider', default='microsoft')
    parser.add_argument('--langkey', default='lang')
    parser.add_argument('--translate-key', default='translation')
    parser.add_argument(
      '--translate-message',
      default='Translated by @Provider from @source using @repo on @Date'
    )
    parser.add_argument('--do-not-translate-frontmatter-double-quote',
      action='store_true',
      default=False
    )
    parser.add_argument('--do-not-translate-frontmatter', type=json.loads, default=[])
    parser.add_argument('--do-not-translate-regex', action='store_true', default=False)
    parser.add_argument('--remove-span-translate-no', action='store_true', default=False)
    parser.add_argument('--force-if-same-hash', action='store_true', default=False)

    args = parser.parse_args()

    # Simulate reading markdown content (you'd actually load the file)
    with open(args.source, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Extract and update frontmatter to handle langkey
    frontmatter = utilities.extract_frontmatter(markdown_content)
    if frontmatter is None:
        frontmatter = {}

    # Update langkey in frontmatter with no-translate span
    frontmatter[args.langkey] = (
        '<span translate="no">__START_NO_TRANSLATE__'
        + args.dest_lang
        + '__END_NO_TRANSLATE__</span>'
    )

    # Reconstruct the content with updated frontmatter
    markdown_content = utilities.update_frontmatter(markdown_content, frontmatter)

    preprocessors = []
    postprocessors = []

    # Add 'do-not-translate-frontmatter' if the argument is set
    if args.do_not_translate_frontmatter:
        frontmatter_keys = args.do_not_translate_frontmatter
        preprocessors.append({
            'name': 'do-not-translate-frontmatter',
            'args': {
                'frontmatter': frontmatter_keys
            }
        })

    if args.do_not_translate_frontmatter_double_quote:
        preprocessors.append({
            'name': 'do-not-translate-frontmatter-double-quote',
            'args': {}
        })

    # Add 'do-not-translate-regex' if the argument is set
    if args.do_not_translate_regex:
        preprocessors.append({
            'name': 'do-not-translate-regex',
            'args': {
                'regex': r'^ {4}(?!\s*//).*',
                'description': 'Code line which begins with a comment',
            }
        })

    # Add 'remove-span-translate-no' if the argument is set
    if args.remove_span_translate_no:
        postprocessors.append({
            'name': 'remove-span-translate-no',
            'args': {},
        })

    source_hash = generate_hash(markdown_content)

    dest_file = args.destination
    # If args.force_if_same_hash: This checks if the flag is not false or else
    # env is not dev the only check hash is generated already.

    if not args.force_if_same_hash :
        # Check existing translation
        if check_existing_translation(dest_file, source_hash, args):
            return

    preprocessors.append({
        'name': 'escape-double-slash',
        'args': {}
    })
    postprocessors.append({
        'name': 'unescape-double-slash',
        'args': {}
    })

    utilities.heading('Call to translator')
    result = my_translate.translate({
      'provider': args.provider,
      'text': markdown_content,
      'from_lg': args.source_lang,
      'to': [args.dest_lang],
      'langkey': args.langkey,
      'translate_key': args.translate_key,
      'translate_message': args.translate_message,
      'do_not_translate_frontmatter': args.do_not_translate_frontmatter,
      'preprocessors': preprocessors,
      'postprocessors': postprocessors
    })

    # Extract and write the translated content to the file
    extract_and_write_translation(result, dest_file, args, source_hash)

if __name__ == '__main__':
    main()
