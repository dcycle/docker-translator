"""Adapted from the Microsoft Translator Text API documentation"""

import uuid
# pylint: disable=E0401
import requests
# pylint: disable=E0401
import utilities

def translate(text, from_lg, to):
    """Transalte text from one language to another using Microsoft Translator Text API"""

    endpoint = utilities.env('MS_ENDPOINT')
    location = utilities.env('MS_LOC')
    key = utilities.env('MS_KEY')

    if not endpoint.startswith('https://'):
        raise EnvironmentError('ENDPOINT must start with https://, you gave' + endpoint)

    # location, also known as region.
    # required if you're using a multi-service or regional (not global) resource.
    # It can be found in the Azure portal on the Keys and Endpoint page.

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': from_lg,
        'to': to,
        # Required to use <span translate="no">
        'textType': 'html',
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        # location required if you're using a multi-service or regional (not global) resource.
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4()),
    }

    # You can pass more than one object in body.
    body = [{
        'text': text
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    return request.json()
