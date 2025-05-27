"""
Change "\n" for and escape it.
Microsoft will sometimes remove newlines between spans, which we don't want
"""

# pylint: disable=W0613
def process(text, args):
    """
    Change "\n" and escape it.
    """
    escaped = '<span translate="no">__START_NO_TRANSLATE____NEWLINE____END_NO_TRANSLATE__</span>'
    return text.replace('\n', escaped)
