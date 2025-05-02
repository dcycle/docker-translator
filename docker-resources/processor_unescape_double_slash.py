"""
Change __DOUBLE_SLASH__ for //
Useful for the microsoft provider which seems to remove // entirely, which
we don't want because sometimes our code examples contain comments.
"""

# pylint: disable=W0613
def process(text, args):
    """
    Change __DOUBLE_SLASH__ for //
    """
    return text.replace('__DOUBLE_SLASH__', '//')
