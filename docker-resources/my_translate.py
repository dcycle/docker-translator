"""Adapted from the Microsoft Translator Text API documentation"""

# pylint: disable=E0401
import my_simulated
# pylint: disable=E0401
import my_microsoft
# pylint: disable=E0401
import processor_add_to_start
# pylint: disable=E0401
import processor_do_not_translate_frontmatter
# pylint: disable=E0401
import processor_do_not_translate_regex
# pylint: disable=E0401
import processor_remove_span_translate_no

# pylint: disable=W0613
def translate(data):
    """Translate some text"""

    provider = data['provider']
    text = data['text']
    from_lg = data['from_lg']
    to = data['to']
    preprocessors = data['preprocessors']
    postprocessors = data['postprocessors']

    preprocessed_text = process(text, preprocessors)

    match provider:
        case 'microsoft':
            ret = my_microsoft.translate(preprocessed_text, from_lg, to)
        case 'simulate':
            ret = my_simulated.translate(preprocessed_text, from_lg, to)
        case _:
            raise EnvironmentError('provider must be set in my_transate.translate()')

    for languages in ret['translations']:
        languages['text'] = process(languages['text'], postprocessors)

    return ret

# pylint: disable=W0613
def process(text, processors):
    """Process text using a processor"""
    for pr in processors:
        text = processor(pr).process(text, pr['args'])
    return text

def processor(pr):
    """Get the processor"""
    if not 'name' in pr:
        raise EnvironmentError('no name in processor ' + str(pr))

    match pr['name']:
        case 'add-to-start':
            return processor_add_to_start
        case 'do-not-translate-frontmatter':
            return processor_do_not_translate_frontmatter
        case 'do-not-translate-regex':
            return processor_do_not_translate_regex
        case 'remove-span-translate-no':
            return processor_remove_span_translate_no
        case _:
            raise EnvironmentError('processor must be set in my_translate.' +
            'processor() got ' + pr['name'])
