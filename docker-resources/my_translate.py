"""Adapted from the Microsoft Translator Text API documentation"""

import json
# pylint: disable=E0401
import my_simulated
# pylint: disable=E0401
import utilities
# pylint: disable=E0401
import my_microsoft
# pylint: disable=E0401
import processor_add_to_start
# pylint: disable=E0401
import processor_md_code
# pylint: disable=E0401
import processor_do_not_translate_frontmatter
# pylint: disable=E0401
import processor_translate_frontmatter
# pylint: disable=E0401
import processor_do_not_translate_frontmatter_doublequote
# pylint: disable=E0401
import processor_do_not_translate_regex
# pylint: disable=E0401
import processor_remove_span_translate_no
# pylint: disable=E0401
import processor_remove_span_translate_no_simple
# pylint: disable=E0401
import processor_escape_double_slash
# pylint: disable=E0401
import processor_unescape_double_slash
# pylint: disable=E0401
import processor_escape_newline
# pylint: disable=E0401
import processor_unescape_newline

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
            utilities.log('About to call my_simulated_translate')
            utilities.log(preprocessed_text)
            ret = my_simulated.translate(preprocessed_text, from_lg, to)
        case _:
            raise EnvironmentError('provider must be set in my_transate.translate()')

    check_for_errors(ret)

    for languages in ret[0]['translations']:
        languages['text'] = process(languages['text'], postprocessors)

    return ret

def check_for_errors(ret):
    """If there is no key 0, but there is a key 'error', raise an error,
    that means something went wrong"""
    if not 0 in ret:
        if 'error' in ret:
            print()
            print('The provider did not provide a translation')
            print('possibly because the credentials are not set')
            print('or invalid')
            print()
            print('The provider returned:')
            print()
            print(ret['error'])
            print()
            raise EnvironmentError('Error in translation: ' + str(ret['error']))

# pylint: disable=W0613
def process(text, processors):
    """Process text using a processor"""
    for pr in processors:
        text = processor(pr).process(text, pr['args'])
        utilities.log('Just processed with ' + pr['name'])
        utilities.log(text)
    return text

# pylint: disable=R0911
def processor(pr):
    """Get the processor"""
    if not 'name' in pr:
        raise EnvironmentError('no name in processor ' + str(pr))

    match pr['name']:
        case 'add-to-start':
            return processor_add_to_start
        case 'do-not-translate-frontmatter':
            return processor_do_not_translate_frontmatter
        case 'translate-frontmatter':
            return processor_translate_frontmatter
        case 'do-not-translate-frontmatter-double-quote':
            return processor_do_not_translate_frontmatter_doublequote
        case 'do-not-translate-regex':
            return processor_do_not_translate_regex
        case 'remove-span-translate-no':
            return processor_remove_span_translate_no
        case 'remove-span-translate-no-simple':
            return processor_remove_span_translate_no_simple
        case 'md-code':
            return processor_md_code
        case 'escape-double-slash':
            return processor_escape_double_slash
        case 'unescape-double-slash':
            return processor_unescape_double_slash
        case 'escape-newline':
            return processor_escape_newline
        case 'unescape-newline':
            return processor_unescape_newline
        case _:
            raise EnvironmentError('processor must be set in my_translate.' +
            'processor() got ' + json.dumps(pr['name']))
