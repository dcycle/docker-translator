"""
Change " <span translate="no">__NEWLINE__</span> " for "\n"
Microsoft will sometimes remove newlines between spans, which we don't want
"""

# pylint: disable=W0613
def process(text, args):
    """
    Change " <span translate="no">__NEWLINE__</span> " for "\n"
    """
    escaped = ' <span translate="no">__NEWLINE__</span> '
    return text.replace(escaped, '\n')
