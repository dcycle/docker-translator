"""
Test the file processor_translate_frontmatter.py.
"""

# pylint: disable=E0401
import processor_translate_frontmatter
import tester

def main():
    """
    Process the frontmatter.
    """
    tester.test(
        'basic test',
        processor_translate_frontmatter,
        'basic',
        {},
    )
    tester.test(
        'complex test',
        processor_translate_frontmatter,
        'complex',
        {
            's': '<<',
            'e': '>>',
        },
    )
    tester.test(
        'complex test where certain keys are translated',
        processor_translate_frontmatter,
        'complex_translate_title_and_embedded',
        {
            's': '<<',
            'e': '>>',
            'translate': [
                'title',
                # there are spaces on purpose because this is an embedded
                # key
                '  multiple_embedded',
            ],
        },
    )

if __name__ == '__main__':
    main()
