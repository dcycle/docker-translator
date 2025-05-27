"""
Processes code within Markdown files.
"""

# pylint: disable=E0401
import processor_do_not_translate_regex

# pylint: disable=W0613
def process(text, args):
    """Runs the processor"""
    # Remove <span translate="no">...</span> tags
    processed = text
    processed = processor_do_not_translate_regex.wrap_in_span(
        processed,
        r'^ {4}(?!\s*//).*',
    )
    # If we don't do this, then any line starting with "    //" will become
    # " //" once translated by microsoft.
    processed = processor_do_not_translate_regex.wrap_in_span(
        processed,
        r'^ {4}//',
    )
    return processed
