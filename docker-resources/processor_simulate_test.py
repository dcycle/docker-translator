"""
Test the file processor_translate_frontmatter.py.
"""

# pylint: disable=E0401
import processor_simulate
import tester

def main():
    """
    Process the frontmatter.
    """
    tester.test(
        'basic test',
        processor_simulate,
        'basic',
        {},
    )

if __name__ == '__main__':
    main()
