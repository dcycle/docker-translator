"""Adapted from the Microsoft Translator Text API documentation"""

# pylint: disable=E0401
import re
# pylint: disable=E0401
import my_simulated
# pylint: disable=E0401
import my_microsoft
# pylint: disable=E0401
import processor_add_to_start

# pylint: disable=W0613
# pylint: disable=R0917
# pylint: disable=R0913
def translate(provider, text, from_lg, to, preprocessors, postprocessors):
    """Translate some text"""

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
        case _:
            raise EnvironmentError('processor must be set in my_translate.' +
            'processor() got ' + pr['name'])
