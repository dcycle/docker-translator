"""Simulation of a translation; does nothing"""

import sys
sys.setrecursionlimit(3000)

def replace(text, translate_me=True):
    """Replace all e's, i's, o's, and u's with 'a's, unless inside a no-translate span"""
    if not text:
        return ''

    if translate_me:
        if text.startswith('<span translate="no">'):
            ret = '<span translate="no">' + replace(text[len('<span translate="no">'):], False)
            return ret
        first = text[0]
        first = first.replace('e', 'a')
        first = first.replace('i', 'a')
        first = first.replace('o', 'a')
        first = first.replace('u', 'a')
        first = first.replace('"', '»')
    else:
        if text.startswith('</span>'):
            ret = '</span>' + replace(text[len('</span>'):], True)
            return ret
        first = text[0]

    ret = first + replace(text[1:], translate_me)
    return ret

# pylint: disable=W0613
def translate(text, from_lg, to):
    """Simulation of a translation. Replace all e's with o's"""
    if text == "____Simulate error____":
        return {
            'error': 'Simulated error',
        }

    translations = []
    for lg in to:
        translations.append({
            'text': replace(text),
            'to': lg,
        })
    return [
        {
            'translations': translations,
        },
    ]
