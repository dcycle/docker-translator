"""
A processor wrapper are my_simulated.py.
"""

# pylint: disable=E0401
import my_simulated

# pylint: disable=W0613
def process(text, args=None):
    """
    A processor wrapper are my_simulated.py.
    """
    result = my_simulated.translate(text, 'whatever', ['whatever'])
    return result[0]['translations'][0]['text']
