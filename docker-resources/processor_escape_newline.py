"""
Change "\n" for " <span translate="no">__NEWLINE__</span> "
Microsoft will sometimes remove newlines between spans, which we don't want
"""

# pylint: disable=W0613
def process(text, args):
    """
    Change "\n" for " <span translate="no">__NEWLINE__</span> "
    """
    escaped = ' <span translate="no">__NEWLINE__</span> '
    return text.replace('\n', escaped)
