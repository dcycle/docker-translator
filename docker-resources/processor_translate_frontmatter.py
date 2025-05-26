"""
Processes YAML frontmatter to:
    1. By default, every line in the frontmatter should not be translated.
"""

# pylint: disable=E0401
import utilities

def process(text, args=None):
    """
    Main processor.

    Args:
    - text (str): The raw data.
    - args (dict, optional): Optional arguments for excluding keys and specifying frontmatter keys.

    Returns:
    - str: Processed YAML frontmatter text.
    """
    if args is None:
        args = {}

    if 'translate' not in args:
        args['translate'] = []
    if 's' not in args:
        args['s'] = '<span translate="no">__START_NO_TRANSLATE__'
    if 'e' not in args:
        args['e'] = '__END_NO_TRANSLATE__</span>'

    # Split the text into pre, frontmatter, and post sections
    valid, pre, frontmatter, post = utilities.split_frontmatter(text)

    if not valid:
        return text

    # Process the frontmatter lines
    processed_lines = process_frontmatter(frontmatter, args)

    # Rebuild the full text with processed frontmatter
    processed_frontmatter = '\n'.join(processed_lines)
    return f"{pre}---\n{processed_frontmatter}\n---{post}"

def process_frontmatter(frontmatter, args):
    """
    Processes the frontmatter lines, applying the necessary transformations.

    Args:
    - frontmatter (str): The raw frontmatter section of the YAML text.
    - exclude_keys (list): Keys to exclude from transformation.
    - frontmatter_keys (list): Specific keys to wrap with 'no-translate' spans.

    Returns:
    - list: A list of processed frontmatter lines.
    """
    lines = frontmatter.strip().split('\n')
    processed_lines = []

    for line in lines:
        processed_line = process_line(line, args)
        processed_lines.append(processed_line)

    return processed_lines

# pylint: disable=W0613
def process_line(line, args):
    """
    Processes a single line of frontmatter, applying the 'no-translate' span transformations.

    Args:
    - line (str): A single line of the YAML frontmatter.
    - exclude_keys (list): Keys to exclude from transformation.
    - frontmatter_keys (list): Specific keys to wrap with 'no-translate' spans.

    Returns:
    - str: The processed line.
    """
    # pylint: disable=W0612
    key_part, value_part = line.split(':', 1)

    # Handle quoted values (only after colon)
    if key_part in args['translate']:
        return args['s'] + key_part + ':' + args['e'] + wrap_quoted_values(value_part, args)

    return args['s'] + line + args['e']

def wrap_quoted_values(value_part, args):
    """
    Wraps each double quote (") in the value part of a line in a no-translate span.
    Skips wrapping if the value is already a fully-wrapped no-translate span.
    """
    # Split into key and value

    # Replace each double quote character " with wrapped version
    quote_wrapper = args['s'] + '"' + args['e']
    return value_part.replace('"', quote_wrapper)
