"""
Processor that adds text to the end of the text
Exists just to demo what a processor does
"""

def process(text, args):
    """Runs the processor"""
    if not args['add']:
        return text
    return text + args['add']
