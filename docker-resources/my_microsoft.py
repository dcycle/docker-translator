"""Adapted from the Microsoft Translator Text API documentation"""

def translate(text, from_lg, to):
    """Transalte text from one language to another using Microsoft Translator Text API"""
    import json
    import os
    import uuid
    import requests
    import utilities

    ENDPOINT = utilities.env('MS_ENDPOINT')
    LOCATION = utilities.env('MS_LOC')
    KEY = utilities.env('MS_KEY')

    if not ENDPOINT.startswith('https://'):
        raise EnvironmentError('ENDPOINT must start with https://, you gave' + ENDPOINT)

    # location, also known as region.
    # required if you're using a multi-service or regional (not global) resource.
    # It can be found in the Azure portal on the Keys and Endpoint page.

    PATH = '/translate'
    CONSTRUCTED_URL = ENDPOINT + PATH

    params = {
        'api-version': '3.0',
        'from': from_lg,
        'to': to,
        # Required to use <span translate="no">
        'textType': 'html',
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
        'text': text
    }]

    request = requests.post(CONSTRUCTED_URL, params=params, headers=headers, json=body)
    return request.json()
