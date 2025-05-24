"""General utilities"""

# pylint: disable=E0401
import os
# pylint: disable=E0401
import re

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

def log(text):
    """Print debug information if debug is set"""
    if env('DEBUG', False):
        print(text)

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
    """Extract YAML frontmatter from markdown content without using yaml.load"""
    frontmatter = {}
    pattern = r'^---\n(.*?)\n---\n'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        frontmatter_str = match.group(1)
        lines = frontmatter_str.strip().split('\n')
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip()
    return frontmatter

def dict_to_yaml(data, indent=0):
    """Convert a dict to YAML (supports nested dictionaries and lists)"""
    lines = []
    indent_str = '  ' * indent
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{indent_str}{key}:")
            for subkey, subvalue in value.items():
                lines.append(f"{indent_str}  {subkey}: {subvalue}")
        elif isinstance(value, list):
            lines.append(f"{indent_str}{key}:")
            for item in value:
                if isinstance(item, dict):
                    lines.append(f"{indent_str}-")
                    for subkey, subvalue in item.items():
                        lines.append(f"{indent_str}  {subkey}: {subvalue}")
                else:
                    lines.append(f"{indent_str}- {item}")
        else:
            lines.append(f"{indent_str}{key}: {value}")
    return '\n'.join(lines)


def update_frontmatter(content, updates):
    """Update YAML frontmatter in markdown content without using yaml.dump"""
    pattern = r'^(---\n.*?\n---\n)'
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        new_frontmatter = dict_to_yaml(updates)
        return f"---\n{new_frontmatter}\n---\n{content}"

    existing = match.group(1)
    current = extract_frontmatter(content)
    current.update(updates)
    new_frontmatter = dict_to_yaml(current)
    return content.replace(existing, f"---\n{new_frontmatter}\n---\n")
