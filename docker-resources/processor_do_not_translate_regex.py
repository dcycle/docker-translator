"""
Processor that handles do-not-translate-regex which adds wrapper
<span translate="no">__START_NO_TRANSLATE__....__END_NO_TRANSLATE__</span> around regex matched text
"""

# pylint: disable=E0401
import re

# pylint: disable=W0613
def wrap_in_span(text, pattern):
    """
    Function to wrap the matched text in 
    <span translate="no">__START_NO_TRANSLATE__....__END_NO_TRANSLATE__</span>
    """
    # Compile the regex pattern
    compiled_pattern = re.compile(pattern, re.MULTILINE)

    # Replace all matches in the text with wrapped <span> tags
    wrapped_text = compiled_pattern.sub(
        r'<span translate="no">__START_NO_TRANSLATE__\g<0>__END_NO_TRANSLATE__</span>',
        text
    )

    return wrapped_text

def process(text, args):
    """Adds a no translate wrapper Regular expression based around text"""
    regex = args.get('regex')

    if regex:
        # Apply the regex wrap function
        text = wrap_in_span(text, regex)

    return text
