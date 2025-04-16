"""Utilities."""

import os
import importlib.machinery

def env(var, default=None):
    """Get environment variable; throw error if not set if default is None."""
    candidate = os.getenv(var)
    if candidate is None or candidate == '':
        if default is not None:
            return default
        print(13)
        raise EnvironmentError(f"Environment variable {var} not set, please see README.md")
    return candidate

def readFile(filename):
    f = open(filename, "r")
    return f.read()

def import_module(module):
    loader = importlib.machinery.SourceFileLoader('a_b', module)
    loader.load_module()
    return module

def pretty_print(json_obj):
    """Pretty print JSON."""
    import json
    print(json.dumps(json_obj, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
