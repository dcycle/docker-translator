"""Adapted from the Microsoft Translator Text API documentation"""

# pylint: disable=E0401
import my_simulated
# pylint: disable=E0401
import my_microsoft

# pylint: disable=W0613
# pylint: disable=R0917
# pylint: disable=R0913
def translate(provider, text, from_lg, to, preprocessors, postprocessors):
    """Translate some text"""

    process(text, preprocessors)

    match provider:
        case 'microsoft':
            ret = my_microsoft.translate(text, from_lg, to)
        case 'simulate':
            ret = my_simulated.translate(text, from_lg, to)
        case _:
            raise EnvironmentError('provider must be set in my_transate.translate()')

    return ret

# pylint: disable=W0613
def process(text, processors):
    """Process text using a processor"""
    return text
