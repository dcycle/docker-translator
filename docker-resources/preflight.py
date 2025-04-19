"""All preflighting code"""

import os
import sys
# pylint: disable=E0401
import my_translate
# pylint: disable=E0401
import utilities

missing_packages = []
missing_env_vars = []
network_errors = []

def errors_exist():
    """Check if errors exist"""
    return len(missing_packages) or len(missing_env_vars) or len(network_errors)

def heading(text):
    """Print a heading"""
    print('')
    print('####')
    print('# ' + text)
    print('####')
    print('')

heading('Preflight check')

try:
    # pylint: disable=W0611
    # pylint: disable=E0401
    import requests
    print('[ok] packages requests found')
except ImportError:
    missing_packages.append('requests')
    print('[error] packages requests not found')

for env_var in ['MS_ENDPOINT', 'MS_LOC', 'MS_KEY']:
    if utilities.env(env_var) is None:
        print('[error] environment variable ' + env_var + ' not found')
        missing_env_vars.append(env_var)
    else:
        print('[ok] environment variable ' + env_var + ' found')

if errors_exist():
    heading('Some errors were found')
else:
    heading('No errors were found')

for missing_package in missing_packages:
    heading('Missing Package ' + missing_package)
    print('You can fix this by running one of the following depending on your environment:')
    print('   ' + 'pip install ' + missing_package)
    print('   ' + 'pip3 install ' + missing_package)
    print('')
    print('Although we recommend running this script in Docker as per the README.md file')
    print('')

for missing_env_var in missing_env_vars:
    heading('[error] missing env var: ' + missing_env_var)
    print('')
    print('See README.md on how to fix this')
    print('')

if errors_exist():
    sys.exit(os.EX_CONFIG)

preprocessors = []
postprocessors = []
if utilities.env('MS_SIMULATE', False):
    PROVIDER = 'simulate'
else:
    PROVIDER = 'microsoft'

heading('Call to translator')
utilities.pretty_print(my_translate.translate({
    'provider': PROVIDER,
    'text': 'Three can keep a secret, if two of them are dead.',
    'from_lg': 'en',
    'to': ['es', 'fr'],
    'preprocessors': preprocessors,
    'postprocessors': postprocessors
  }
))

utilities.pretty_print(my_translate.translate({
    'provider': PROVIDER,
    'text': """
    This is an example of some text which contains a code block

      $household->dogs();
    """,
    'from_lg': 'en',
    'to': ['fr'],
    'preprocessors': preprocessors,
    'postprocessors': postprocessors
  }
))

utilities.pretty_print(my_translate.translate({
    'provider': PROVIDER,
    'text': """
    This is an example of some text which contains a code block

      <span translate="no">$household->dogs()</span>;
    """,
    'from_lg': 'en',
    'to': ['fr'],
    'preprocessors': preprocessors,
    'postprocessors': postprocessors
  }
))

utilities.pretty_print(my_translate.translate({
    'provider': PROVIDER,
    'text': """
    ----
    title: "My trip on the Nile"
    ----
    It was during a hot day on the boat "The Queen of Egypt" that I wrote this source code:

        $dogs = $household->dogs();
        // Display number of dogs
        echo "We have " . $dogs->count() . "dogs";
    """,
    'from_lg': 'en',
    'to': ['fr'],
    'preprocessors': preprocessors,
    'postprocessors': postprocessors
  }
))

# https://learn.microsoft.com/en-us/azure/ai-services/translator/text-translation/how-to/prevent-translation
# Only works if the textType is set to html, which it is in the file
# my_microsoft.py
utilities.pretty_print(my_translate.translate({
    'provider': PROVIDER,
    'text': """
    ----
    <span translate="no">title</span>: "My trip on the Nile"
    ----
    It was during a hot day on the boat
    "<span translate="no">The Queen of Egypt</span>" that I wrote this source
    code:

        <span translate="no">$dogs = $household->dogs();</span>
        // Display number of dogs
        <span translate="no">echo "We have " . $dogs->count() . "dogs";</span>
    """,
    'from_lg': 'en',
    'to': ['fr'],
    'preprocessors': preprocessors,
    'postprocessors': postprocessors
  }
))

utilities.pretty_print(my_translate.translate({
    'provider': PROVIDER,
    'text': """
    this is a test with pre- and post-processors
    """,
    'from_lg': 'en',
    'to': ['fr'],
    'preprocessors': [
      {
        'name' : 'add-to-start',
        'args' : {
          'add': 'THIS WAS ADDED BY THE PREPROCESSOR ',
        },
      },
    ],
    'postprocessors': [
      {
        'name' : 'add-to-start',
        'args' : {
          'add': 'THIS WAS ADDED BY THE POSTPROCESSOR ',
        },
      }
    ]
  }
))

# author key in frontmatter shouldn't be translated
utilities.pretty_print(my_translate.translate({
    'provider': PROVIDER,
    'text': """
    ---
    title: "My trip on the Nile"
    author: "abcd"
    ---
    It was during a hot day on the boat "The Queen of Egypt" that I wrote this source code:

        $dogs = $household->dogs();
        // Display number of dogs
        echo "We have " . $dogs->count() . "dogs";

    """,
    'from_lg': 'en',
    'to': ['fr'],
    # pylint: disable=E0401
    'preprocessors': [
      {
        # pylint: disable=E0401
        'name' : 'do-not-translate-frontmatter',
        # pylint: disable=E0401
        'args' : {
          'frontmatter': [
            'author',
          ]
        },
      }
    ],
    'postprocessors': [
      {
        'name' : 'remove-span-translate-no',
        'args' : {},
      }
    ]
  }
))

# title, description and regex matched text shouldn't be translated.
# Ensure regex matches your text other wise we will end up in a error
utilities.pretty_print(my_translate.translate({
    'provider': PROVIDER,
    'text': """
    ---
    title: "My trip on the Nile"
    description: "It was during a hot day on the boat that I wrote this source code"
    ---
    It was during a hot day on the boat "The Queen of Egypt" that I wrote this source code:

        $dogs = $household->dogs();
        // Display number of dogs
        echo "We have " . $dogs->count() . "dogs";

    """,
    'from_lg': 'en',
    'to': ['fr'],
    # pylint: disable=E0401
    'preprocessors': [
      {
        # pylint: disable=E0401
        'name' : 'do-not-translate-frontmatter',
        # pylint: disable=E0401
        'args' : {
          'frontmatter': [
            'title',
            'description'
          ]
        },
      },
      {
        # pylint: disable=E0401
        'name' : 'do-not-translate-regex',
        # pylint: disable=E0401
        'args' : {
          # pylint: disable=E0401
          'regex': r'^ {8}(?!\s*//).*',
          'description': 'Code line which begins with a comment',
        },
      },
    ],
    'postprocessors': [
      {
        'name' : 'remove-span-translate-no',
        'args' : {},
      }
    ]
  }
))

utilities.pretty_print(my_translate.translate({
    'provider': PROVIDER,
    'text': """
    ---
    title: "My trip on the Nile"
    ---
    It was during a hot day on the boat "The Queen of Egypt" that I wrote this source code:

        $dogs = $household->dogs();
        // Display number of dogs
        echo "We have " . $dogs->count() . "dogs";

    """,
    'from_lg': 'en',
    'to': ['fr'],
    # pylint: disable=E0401
    'preprocessors': [
      {
        # pylint: disable=E0401
        'name' : 'do-not-translate-regex',
        # pylint: disable=E0401
        'args' : {
          # pylint: disable=E0401
          'regex': r'^ {8}(?!\s*//).*',
          'description': 'Code line which begins with a comment',
        },
      },
    ],
    'postprocessors': [
      {
        'name' : 'remove-span-translate-no',
        'args' : {},
      }
    ]
  }
))
