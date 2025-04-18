"""
Processor that removes
<span translate="no">__START_NO_TRANSLATE__...__END_NO_TRANSLATE__</span> tags
"""

# pylint: disable=E0401
import re

# pylint: disable=W0613
def process(text, args):
    """Runs the processor"""
    # Remove <span translate="no">...</span> tags
    text = re.sub(
        r'<span translate="no">__START_NO_TRANSLATE__(.*?)__END_NO_TRANSLATE__</span>', r'\1',
        text
    )

    return text
