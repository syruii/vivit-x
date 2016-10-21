import pprint
from xml.etree import cElementTree
import requests, random


def _imageSearch(args,method,page):
    payload = {'tags': args, 'limit': 50, 'page': 'dapi', 'pid': page, 's': 'post', 'q': 'index'}
    r = requests.get("http://gelbooru.com/index.php", params=payload)
    if r.status_code != 200:
        return -1
    tree = cElementTree.fromstring(r.text)

    results = []
    if method == "nsfw":
        for image in tree.findall('post'):
            if image.get('rating') != 's':
                results.append(image)
    elif method == "sfw":
        for image in tree.findall('post'):
            if image.get('rating') == 's':
                results.append(image)
    else:
        results = tree.findall('post')

    if not results:
        return None

    rand = random.randrange(0, len(results))
    if results[rand].get('file_url'):
        return results[rand].get('file_url')
    else:
        return results[rand].get('source')


def search(method,query,page):
    result = _imageSearch(query,method,page)
    if result is None:
        return "No images found for specified tag(s).",1
    elif result == -1:
        return "An error occurred with the query.", 1
    else:
        return result, 0