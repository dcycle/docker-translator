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

def extract_raw_frontmatter(content):
    """Extract raw frontmatter string from Markdown content."""
    pattern = r'^---\n(.*?)\n---\n'
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1) if match else ""

def parse_yaml_frontmatter(raw_yaml):
    """Parse YAML frontmatter string into a Python dictionary."""
    try:
        return yaml.load(raw_yaml, Loader=SafeLoader) or {}
    except yaml.YAMLError:
        return {}

def get_yaml_lines(raw_yaml):
    """Split raw YAML into lines."""
    return raw_yaml.splitlines()

def is_quoted(value, key, lines):
    """Check if a given key's value is quoted in the raw YAML lines."""
    for line in lines:
        if line.strip().startswith(f"{key}:"):
            _, val_part = line.split(":", 1)
            val_part = val_part.strip()
            return val_part.startswith('"') and val_part.endswith('"')
    return False

def get_quoted_value_from_lines(key, lines):
    """Get the exact quoted value from raw YAML lines."""
    for line in lines:
        if line.strip().startswith(f"{key}:"):
            return line.split(":", 1)[1].strip()
    return None

def preserve_quoted_string_value(key, value, lines):
    """Preserve quotes if they were present in the original YAML."""
    return get_quoted_value_from_lines(key, lines) if is_quoted(value, key, lines) else value

def preserve_quoted_dict_items(item_dict, lines):
    """Preserve quotes for dictionary items inside a list."""
    result = {}
    for key, value in item_dict.items():
        if is_quoted(value, key, lines):
            result[key] = f'"{value}"'
        else:
            result[key] = value
    return result

def preserve_quotes(parsed_data, raw_yaml_lines):
    """Reconstruct parsed data with original quotes preserved from raw YAML."""
    result = {}
    for key, value in parsed_data.items():
        if isinstance(value, str):
            result[key] = preserve_quoted_string_value(key, value, raw_yaml_lines)

        elif isinstance(value, list):
            result[key] = [
                preserve_quoted_dict_items(item, raw_yaml_lines) if isinstance(item, dict) else item
                for item in value
            ]

        else:
            result[key] = value
    return result

def extract_frontmatter(content):
    """High-level function to extract and parse YAML frontmatter with quotes preserved."""
    raw_yaml = extract_raw_frontmatter(content)
    if not raw_yaml:
        return {}
    parsed_data = parse_yaml_frontmatter(raw_yaml)
    yaml_lines = get_yaml_lines(raw_yaml)
    return preserve_quotes(parsed_data, yaml_lines)

def update_frontmatter(content, updates):
    """Update frontmatter with new key-value pairs"""
    pattern = r'^(---\n.*?\n---\n)'
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        # No frontmatter exists, create it
        new_frontmatter = yaml.dump(
            current,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            # prevent multiline wrapping
            width=float("inf")
        )
        return f"---\n{new_frontmatter}---\n{content}"

    # Update existing frontmatter
    existing = match.group(1)
    try:
        current = yaml.load(existing[4:-4], Loader=SafeLoader) or {}
        current.update(updates)
        new_frontmatter = yaml.dump(
            current,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            # prevent multiline wrapping
            width=float("inf")
        )
        return content.replace(existing, f"---\n{new_frontmatter}---\n")
    except yaml.YAMLError:
        return content
