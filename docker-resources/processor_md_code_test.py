"""
Test the file processor_md_code.py.
"""

# pylint: disable=E0401
import processor_md_code
import tester

def main():
    """
    Test processor_md_code.
    """
    tester.test(
        'basic test',
        processor_md_code,
        'basic',
        {},
    )
    tester.test(
        'code test',
        processor_md_code,
        'code',
        {},
    )

if __name__ == '__main__':
    main()
