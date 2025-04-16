"""Simulation of a translation; does nothing"""

def replace(text, translate = True):
    """Replace all e's with o's"""
    if not len(text):
        return ''
    if translate:
        if text.startswith('<span translate="no">'):
            return replace(text, False)
        else:
            first = text[0]
            first = first.replace('e', 'a')
            first = first.replace('i', 'a')
            first = first.replace('o', 'a')
            first = first.replace('u', 'a')
    else:
        if text.startswith('</span>'):
            return replace(text, True)
        else:
            first = text[0]
    return first + replace(text[1:], translate)

def translate(text, from_lg, to):
    """Simulation of a translation. Replace all e's with o's"""
    translations = list()
    for lg in to:
        translations.append({
            'text': replace(text),
            'to': lg,
        })
    return {
        'translations': translations
    }
