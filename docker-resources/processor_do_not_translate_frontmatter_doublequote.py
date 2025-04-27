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

    exclude_keys = args.get('exclude', [])
    frontmatter_keys = args.get('frontmatter', [])

    # Split the text into pre, frontmatter, and post sections
    pre, frontmatter, post = split_frontmatter(text)

    # Process the frontmatter lines
    processed_lines = process_frontmatter(frontmatter, exclude_keys, frontmatter_keys)

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

def process_frontmatter(frontmatter, exclude_keys, frontmatter_keys):
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
        processed_line = process_line(line, exclude_keys, frontmatter_keys)
        processed_lines.append(processed_line)

    return processed_lines

def process_line(line, exclude_keys, frontmatter_keys):
    """
    Processes a single line of frontmatter, applying the 'no-translate' span transformations.

    Args:
    - line (str): A single line of the YAML frontmatter.
    - exclude_keys (list): Keys to exclude from transformation.
    - frontmatter_keys (list): Specific keys to wrap with 'no-translate' spans.

    Returns:
    - str: The processed line.
    """
    original_line = line.rstrip()
    processed_line = line

    # Check if the key is in the excluded list
    for key in exclude_keys:
        if re.match(rf'^\s*{re.escape(key)}\s*:', original_line):
            processed_line = wrap_in_no_translate_span(original_line)
            break
    else:
        # Handle key wrapping (key name only, without colon)
        if not exclude_keys or any(
            re.match(rf'^\s*{re.escape(key)}\s*:', original_line) for key in frontmatter_keys
        ):
            processed_line = wrap_key_in_no_translate_span(line)

        # Handle quoted values (only after colon)
        if ':' in processed_line:
            processed_line = wrap_quoted_values(processed_line)

    return processed_line

def wrap_in_no_translate_span(line):
    """
    Wraps the entire line in a 'no-translate' span.

    Args:
    - line (str): The line to wrap.

    Returns:
    - str: The line wrapped in a 'no-translate' span.
    """
    return f'<span translate="no">__START_NO_TRANSLATE__{line}__END_NO_TRANSLATE__</span>'

def wrap_key_in_no_translate_span(line):
    """
    Wraps the key portion (before the colon) of the line in a 'no-translate' span.

    Args:
    - line (str): The line to wrap.

    Returns:
    - str: The line with the key wrapped in a 'no-translate' span.
    """
    return re.sub(
        r'^(\s*)([^:#"\'\s]+)(\s*:)',
        r'\1<span translate="no">__START_NO_TRANSLATE__\2__END_NO_TRANSLATE__</span>\3',
        line
    )

def wrap_quoted_values(line):
    """
    Wraps the quoted values in a line (after the colon) in a 'no-translate' span.

    Args:
    - line (str): The line to wrap.

    Returns:
    - str: The line with quoted values wrapped in a 'no-translate' span.
    """
    key_part, value_part = line.split(':', 1)

    # Define the pattern for matching quoted values
    pattern = r'("[^"]*")'

    # Define the replacement function for quoted values
    def wrap_quoted_value(match):
        # Get the matched quoted string (without the surrounding quotes)
        quoted_value = match.group(1)[1:-1]
        # Wrap the quotes and the quoted value in no-translate spans
        return (
            '<span translate="no">__START_NO_TRANSLATE__"__END_NO_TRANSLATE__</span>'
            + quoted_value +
            '<span translate="no">__START_NO_TRANSLATE__"__END_NO_TRANSLATE__</span>'
        )

    # Apply the regex substitution using the pattern and replacement function
    value_part = re.sub(pattern, wrap_quoted_value, value_part)

    return f'{key_part}:{value_part}'
