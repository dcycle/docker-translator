"""Adapted from the Microsoft Translator Text API documentation"""

def translate(provider, text, from_lg, to, preprocessors, postprocessors):
    import my_simulated
    import my_microsoft

    process(text, preprocessors)

    match provider:
        case 'microsoft':
            ret = my_microsoft.translate(text, from_lg, to)
        case 'simulate':
            ret = my_simulated.translate(text, from_lg, to)
        case _:
            raise EnvironmentError('provider must be set in my_transate.translate()')

    return ret

def process(text, processors):
    return text
