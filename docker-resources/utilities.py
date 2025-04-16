"""General utilities"""

import os

def env(var, default=None):
    """Get environment variable; throw error if not set if default is None."""
    candidate = os.getenv(var)
    if candidate is None or candidate == '':
        if default is not None:
            return default
        print(13)
        raise EnvironmentError(f"Environment variable {var} not set, please see README.md")
    return candidate

def read_file(filename):
    """Read a file's contents"""
    with open(filename, encoding="utf-8") as f:
        f.read()

def pretty_print(json_obj):
    """Pretty print JSON."""
    # pylint: disable=C0415
    import json
    print(
        json.dumps(
            json_obj,
            sort_keys=True,
            ensure_ascii=False,
            indent=4,
            separators=(',', ': '),
        ),
    )
