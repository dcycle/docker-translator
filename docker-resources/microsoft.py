"""Adapted from the Microsoft Translator Text API documentation"""
import json
import os
import uuid
# pylint: disable=E0401
import requests

def env_var(var, default=None):
    """Get environment variable; throw error if not set."""
    candidate = os.environ.get(var)
    if candidate is None:
        if default is not None:
            return default
        raise EnvironmentError(f"Environment variable {var} not set, please see README.md")
    return candidate

# Add your key and endpoint
KEY = env_var('MS_KEY')
ENDPOINT = env_var('MS_ENDPOINT')

# location, also known as region.
# required if you're using a multi-service or regional (not global) resource.
# It can be found in the Azure portal on the Keys and Endpoint page.
LOCATION = env_var('MS_LOC')
TARGET = env_var('MS_TARGET')

PATH = '/translate'
CONSTRUCTED_URL = ENDPOINT + PATH

print(CONSTRUCTED_URL)

params = {
    'api-version': '3.0',
    'from': 'en',
    'to': TARGET.split(';'),
}

headers = {
    'Ocp-Apim-Subscription-Key': KEY,
    # location required if you're using a multi-service or regional (not global) resource.
    'Ocp-Apim-Subscription-Region': LOCATION,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4()),
}

# You can pass more than one object in body.
body = [{
    'text': 'I would really like to drive your car around the block a few times!'
}]

request = requests.post(CONSTRUCTED_URL, params=params, headers=headers, json=body)
response = request.json()

print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
