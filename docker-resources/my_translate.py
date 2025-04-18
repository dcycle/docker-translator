"""Adapted from the Microsoft Translator Text API documentation"""

# pylint: disable=E0401
import re
# pylint: disable=E0401
import my_simulated
# pylint: disable=E0401
import my_microsoft

# pylint: disable=W0613
# pylint: disable=R0917
# pylint: disable=R0913
def translate(provider, text, from_lg, to, preprocessors, postprocessors):
    """Translate some text"""

    apply_preprocessors(text, preprocessors)

    match provider:
        case 'microsoft':
            ret = my_microsoft.translate(text, from_lg, to)
        case 'simulate':
            ret = my_simulated.translate(text, from_lg, to)
        case _:
            raise EnvironmentError('provider must be set in my_transate.translate()')

    apply_postprocessors(text, postprocessors)
    return ret

# pylint: disable=W0613
def apply_frontmatter_no_translate(text, frontmatter_fields):
    """Wrap specified frontmatter field names with <span translate="no">."""
    for field in frontmatter_fields:
        # Define the regex pattern to match the dynamic field_name followed by a colon
        pattern = rf'(\s*)({field}):'

        # Replace the field_name with the new format, keeping the value intact
        text = re.sub(pattern, r'\1<span translate="no">\2:</span>', text)

    return text

# pylint: disable=W0613
def wrap_in_span(text, pattern):
    """Function to wrap the matched text in <span translate="no"></span>"""
    # Compile the regex pattern
    compiled_pattern = re.compile(pattern, re.MULTILINE)

    # Replace all matches in the text with wrapped <span> tags
    # Function to wrap match inside <span> and preserve leading spaces
    def wrap_with_spaces(match):
        matched_text = match.group(0)
        # Get the number of leading spaces
        leading_spaces = len(matched_text) - len(matched_text.lstrip())
        return ' ' * leading_spaces + f'<span translate="no">{matched_text.strip()}</span>'

    # Replace all matches in the text with wrapped <span> tags
    wrapped_text = compiled_pattern.sub(wrap_with_spaces, text)

    return wrapped_text

# pylint: disable=W0613
def apply_preprocessors(text, preprocessors):
    """Apply preprocessing steps to the text."""
    for processor in preprocessors:
        name = processor['name']
        args = processor['args']

        if name == 'do-not-translate-regex':
            regex = args.get('regex')

            if regex:
                # Apply the regex wrap function
                text = wrap_in_span(text, regex)

        if name == 'do-not-translate-frontmatter':
            text = apply_frontmatter_no_translate(text, args['frontmatter'])

    print("--- after preprocess ---", text)
    return text

# pylint: disable=W0613
def apply_postprocessors(text, postprocessors):
    """Apply postprocessing steps to the text."""
    for processor in postprocessors:
        name = processor['name']
        # args = processor['args']

        if name == 'remove-span-translate-no':
            # Remove <span translate="no">...</span> tags
            text = re.sub(r'<span translate="no">(.*?)</span>', r'\1', text)

    return text
