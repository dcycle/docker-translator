"""
Testing utilities.
"""

import json
import os.path

def read(filename):
    """
    Read a file's contents.
    """
    base = os.path.dirname(os.path.abspath(__file__))

    filename = os.path.join(base, filename)

    with open(filename, encoding="utf-8") as file:
        return file.read()

def test(processor, textfile, args):
    """
    Test a processor.
    """
    text = read(processor.__name__ + '_test/' + textfile + '.txt')
    expected = read(processor.__name__ + '_test/' + textfile + '_expected.txt')

    print('testing ' + processor.__name__)
    print('text is')
    print(text)
    print('args are')
    print(args)
    print('expected is')
    print(json.dumps(expected))
    print(expected)
    result = processor.process(text, args)
    print('result is')
    print(json.dumps(result))
    print(result)
    if result != expected:
        raise AssertionError('Test failed')
