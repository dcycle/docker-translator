"""
Processor wraps <span translate="no">__START_NO_TRANSLATE__....__END_NO_TRANSLATE__</span> around
Regex pattern matched dynamic field name of frontmatter followed by a colon
"""

# pylint: disable=E0401
import re

def process(text, args):
    """
    Wrap specified frontmatter field names with
    <span translate="no">__START_NO_TRANSLATE__....__END_NO_TRANSLATE__</span>.
    """
    for field in args['frontmatter']:
        # Define the regex pattern to match the dynamic field_name followed by a colon
        pattern = rf'(\s*)({field}):'

        # Replace the field_name with the new format, keeping the value intact
        text = re.sub(
            pattern,
            r'\1<span translate="no">__START_NO_TRANSLATE__\2:__END_NO_TRANSLATE__</span>',
            text
        )

    return text
