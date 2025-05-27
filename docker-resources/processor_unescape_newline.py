"""
Change unescapted version of "\n"
Microsoft will sometimes remove newlines between spans, which we don't want
"""

# pylint: disable=W0613
def process(text, args):
    """
    Change unescapted version of "\n"
    """
    processed = text
    escaped = '<span translate="no">__START_NO_TRANSLATE____NEWLINE____END_NO_TRANSLATE__</span>'
    processed = processed.replace(escaped, '\n')
    # Possible that a previous procssor has alraedy replaced span translate no,
    # so we also check for __NEWLINE__
    escaped = '__NEWLINE__'
    processed = processed.replace(escaped, '\n')
    return processed
