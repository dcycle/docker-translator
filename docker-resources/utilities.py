"""General utilities"""

# pylint: disable=E0401
import os
# pylint: disable=E0401
import re
# pylint: disable=E0401
import yaml
# pylint: disable=E0401
from yaml import SafeLoader

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

def heading(text):
    """Print a heading"""
    print('')
    print('####')
    print('# ' + text)
    print('####')
    print('')

def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown content"""
    frontmatter = {}
    pattern = r'^---\n(.*?)\n---\n'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        frontmatter_str = match.group(1)
        try:
            frontmatter = yaml.load(frontmatter_str, Loader=SafeLoader) or {}
        except yaml.YAMLError:
            pass
    return frontmatter

def update_frontmatter(content, updates):
    """Update frontmatter with new key-value pairs"""
    pattern = r'^(---\n.*?\n---\n)'
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        # No frontmatter exists, create it
        new_frontmatter = yaml.dump(updates, allow_unicode=True, default_flow_style=False)
        return f"---\n{new_frontmatter}---\n{content}"

    # Update existing frontmatter
    existing = match.group(1)
    try:
        current = yaml.load(existing[4:-4], Loader=SafeLoader) or {}
        current.update(updates)
        new_frontmatter = yaml.dump(current, allow_unicode=True, default_flow_style=False)
        return content.replace(existing, f"---\n{new_frontmatter}---\n")
    except yaml.YAMLError:
        return content
