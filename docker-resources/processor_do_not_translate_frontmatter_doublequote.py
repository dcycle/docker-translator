"""
Processes YAML frontmatter to:
    1. When exclude_keys is empty: Wrap all keys (without colons) in no-translate spans
    2. When exclude_keys specified: Only wrap specified keys
    3. Wrap only quotation marks in values (after colon)
    4. Fully exclude specified keys (entire line)
"""

# pylint: disable=E0401
import re

def process(text, args=None):
    """
    Main processor function that breaks down the YAML frontmatter, processes keys,
    values, and applies 'no-translate' spans as needed.

    Args:
    - text (str): The raw YAML frontmatter text to process.
    - args (dict, optional): Optional arguments for excluding keys and specifying frontmatter keys.

    Returns:
    - str: Processed YAML frontmatter text.
    """
    if args is None:
        args = {}

    # Split the text into pre, frontmatter, and post sections
    pre, frontmatter, post = split_frontmatter(text)

    # Process the frontmatter lines
    processed_lines = process_frontmatter(frontmatter)

    # Rebuild the full text with processed frontmatter
    processed_frontmatter = '\n'.join(processed_lines)
    return f"{pre}---\n{processed_frontmatter}\n---{post}"

def split_frontmatter(text):
    """
    Splits the YAML text into three parts: pre, frontmatter, and post.

    Args:
    - text (str): The raw YAML text.

    Returns:
    - tuple: A tuple of (pre, frontmatter, post) parts of the text.
    """
    parts = text.split('---')
    if len(parts) < 3:
        return text, '', ''
    pre = parts[0]
    frontmatter = parts[1]
    post = '---'.join(parts[2:])
    return pre, frontmatter, post

def process_frontmatter(frontmatter):
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
        processed_line = process_line(line)
        processed_lines.append(processed_line)

    return processed_lines

def process_line(line):
    """
    Processes a single line of frontmatter, applying the 'no-translate' span transformations.

    Args:
    - line (str): A single line of the YAML frontmatter.
    - exclude_keys (list): Keys to exclude from transformation.
    - frontmatter_keys (list): Specific keys to wrap with 'no-translate' spans.

    Returns:
    - str: The processed line.
    """
    processed_line = line.rstrip()

    # Handle quoted values (only after colon)
    if ':' in processed_line:
        processed_line = wrap_quoted_values(processed_line)

    return processed_line

def wrap_quoted_values(line):
    """
    Wraps each double quote (") in the value part of a line in a no-translate span.
    Skips wrapping if the value is already a fully-wrapped no-translate span.
    """
    # Split into key and value
    key_part, value_part = line.split(':', 1)
    value_part = value_part.strip()

    # If value part is already fully wrapped in a no-translate span, skip it
    already_wrapped_pattern = (
        r'^<span translate="no">'
        r'__START_NO_TRANSLATE__.*?__END_NO_TRANSLATE__'
        r'</span>$'
    )

    if re.fullmatch(already_wrapped_pattern, value_part):
        return f'{key_part}: {value_part}'

    # Replace each double quote character " with wrapped version
    quote_wrapper = '<span translate="no">__START_NO_TRANSLATE__"__END_NO_TRANSLATE__</span>'
    value_part = value_part.replace('"', quote_wrapper)

    return f'{key_part}: {value_part}'
