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
        processor_translate_frontmatter,
        'basic',
        {},
    )
    tester.test(
        processor_translate_frontmatter,
        'complex',
        {},
    )

if __name__ == '__main__':
    main()
