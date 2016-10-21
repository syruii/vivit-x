from googleapiclient.discovery import build
import json, urllib, pprint

with open('credentials.json') as json_data:
    creds = json.load(json_data)
service = build('youtube','v3',creds['youtube'])

def search(query,num=1):
    query = urllib.parse.quote_plus(query)
    request = service.search().list(q=query, type="video", maxResults=10)
    response = request.execute()
    pprint.pprint(response)