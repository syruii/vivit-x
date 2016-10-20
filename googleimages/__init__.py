import json

import requests


def _imageSearch(query, creds):
    num = 10
    payload = {'q': query, 'cx': creds['searchcx'], 'num': num, 'searchType': 'image', 'start': 1,
               'key': creds['googleimage']}
    r = requests.get("https://www.googleapis.com/customsearch/v1", params=payload)
    image = json.loads(r.text)
    return image


def search(query, creds, num):
    image = _imageSearch(query, creds)
    print(num)
    if 'items' in image.keys():
        return (image['items'][num]['link'], 0)
    else:
        print(image)
        if 'error' in image.keys():
            return (image['error']['message'], 1)
        return ('No results found.', 1)
