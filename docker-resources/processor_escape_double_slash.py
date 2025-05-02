"""
Change // for __DOUBLE_SLASH__
Useful for the microsoft provider which seems to remove // entirely, which
we don't want because sometimes our code examples contain comments.
"""

def process(text):
    """
    Change // for __DOUBLE_SLASH__
    """
    return text.replace('//', '__DOUBLE_SLASH__')
