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
import my_translate
# pylint: disable=E0401
import utilities

def generate_hash(content):
    """
    add readme
    """
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def replace_message_placeholders(message, args):
    """
    add readme
    """
    replacements = {
        '@Provider': args.provider,
        '@source': args.source_lang,
        '@repo': 'http://github.com/dcycle/docker-translator',
        '@Date': datetime.now().isoformat()[:10]  # YYYY-MM-DD
    }
    for placeholder, value in replacements.items():
        message = message.replace(placeholder, value)
    return message

def check_existing_translation(dest_file, source_hash, args):
    """
    add readme
    """
    if not os.path.exists(dest_file):
        return False

    with open(dest_file, 'r', encoding='utf-8') as f:
        content = f.read()
        frontmatter = utilities.extract_frontmatter(content)

        if frontmatter.get(args.translate_key, {}).get('hash') == source_hash:
            print(f"Did not translate because source hash of {args.source}, {source_hash}, "
                  f"is the same as the source hash key in the existing destination file")
            return True
    return False

def extract_and_write_translation(result, dest_file, args, source_hash):
    """Extract translation and write to file with updated frontmatter"""
    translated_text = result['translations'][0]['text']

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

    # Preserve do-not-translate fields
    for key in args.do_not_translate_frontmatter:
        if key in existing_frontmatter:
            translation_metadata[key] = existing_frontmatter[key]

    # Prepare all frontmatter updates
    updates = {
        args.langkey: args.dest_lang,  # Language key
        args.translate_key: translation_metadata  # Translation info
    }

    # Update the content
    final_content = utilities.update_frontmatter(translated_text, updates)

    # Write the file
    with open(dest_file, 'w', encoding='utf-8') as out_f:
        out_f.write(final_content)

    print(f"Translation saved to {dest_file}")

def main():
    """
    faklfa;lkdfj
    """
    parser = argparse.ArgumentParser(description='Translate markdown content.')
    parser.add_argument('--source', required=True)
    parser.add_argument('--source-lang', required=True)
    # Add the destination-folder argument
    parser.add_argument('--destination-folder', default=None)
    parser.add_argument('--dest-lang', required=True)
    parser.add_argument('--provider', default='microsoft')
    parser.add_argument('--langkey', default='lang')
    parser.add_argument('--translate-key', default='translation')
    parser.add_argument(
      '--translate-message',
      default='Translated by @Provider from @source using @repo on @Date'
    )
    parser.add_argument('--do-not-translate-frontmatter', nargs='*', default=[])
    parser.add_argument('--do-not-translate-regex', action='store_true', default=False)
    parser.add_argument('--remove-span-translate-no', action='store_true', default=False)

    args = parser.parse_args()

    # Set the destination-folder to the value of --source if not provided
    if args.destination_folder is None:
        args.destination_folder = args.source

    # Simulate reading markdown content (you'd actually load the file)
    with open(args.source, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

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

    # Output the resulting preprocessors and postprocessors for debugging
    print("Preprocessors:")
    for pre in preprocessors:
        print(pre)

    print("\nPostprocessors:")
    for post in postprocessors:
        print(post)

    source_hash = generate_hash(markdown_content)

    # Check existing translation
    dest_file = f"{args.destination_folder}.{args.dest_lang}.md"
    if check_existing_translation(dest_file, source_hash, args):
        return

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

    utilities.pretty_print(result)

    # Extract and write the translated content to the file
    extract_and_write_translation(result, dest_file, args, source_hash)

if __name__ == '__main__':
    main()
