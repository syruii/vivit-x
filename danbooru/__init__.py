import json, pprint
import requests, random


def _imageSearch(args,method,page):
    payload = {'tags': args, 'limit': 50, 'page': page}
    r = requests.get("http://danbooru.donmai.us/posts.json", params=payload)
    if r.status_code != 200:
        return -1
    images = json.loads(r.text)

    if not images:
        return None

    results = []
    if method == "nsfw":
        for image in images:
            if image['rating'] != 's':
                results.append(image)
    elif method == "sfw":
        for image in images:
            if image['rating'] == 's':
                results.append(image)
    else:
        results = images
    rand = random.randrange(0, len(results))
    if 'large_file_url' in results[rand].keys():
        return "https://danbooru.donmai.us" + results[rand]['large_file_url']
    else:
        return results[rand]['source']


def _tagSearch(arg):
    payload = {'search[name_matches]': arg, 'search[hide_empty]': 'yes'}
    r = requests.get("http://danbooru.donmai.us/tags.json", params=payload)

    if r.status_code != 200:
        return -1

    tags = json.loads(r.text)
    if not tags:
        return None
    else:
        return tags


def search(method,query,page):
    result = _imageSearch(query,method,page)
    if result is None:
        return "No images found for specified tag(s).",1
    elif result == -1:
        return "An error occurred with the query.", 1
    else:
        return result, 0


def tagsearch(query):
    result = _tagSearch(query)
    if result is None:
        return "No tags found matching query.", 1
    elif result == -1:
        return "An error occurred with the query.", 1
    else:
        tags = []
        for tag in result:
            _result = "``{}``: {} posts.".format(tag['name'], tag['post_count'])
            tags.append(_result)
        return '\n'.join(tags), 0
