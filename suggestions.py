import csv
import googlemaps
import json
from vocabulary.vocabulary import Vocabulary as vb

gmaps = googlemaps.Client(open('google-api-key.txt', 'r').read())

reserved = []
with open('data/ReservedList.csv', 'r') as cs:
    reserved_temp = list(csv.reader(cs))[1:]
    for sublist in reserved_temp:
        for domain in sublist:
            reserved.append(domain)

registered = []
with open('data/20180222-zone-data.txt', 'r') as f:
    for line in f:
        registered.append(line.split(None, 1)[0])

# address_info = gmaps.reverse_geocode('38.35125,53.593215')

buying_prefixes = []
selling_prefixes = []
service_prefixes = []
cultural_data = {}


def get_locations(location):
    return []


def get_synonyms(customizer):
    return []


def get(website_json):
    website_info = json.loads(website_json)
    location = str(website_info['location']['lat']) + ',' + str(website_info['location']['long'])
    locations = get_locations(location)
    synonyms = get_synonyms(website_info['customizer'])
    prefixes = []

    if website_info['modifier'] == 'buying':
        prefixes = buying_prefixes
    elif website_info['modifier'] == 'selling':
        prefixes = selling_prefixes
    else:
        prefixes = service_prefixes

    suggestions = {}

    for i in range(0, 50):
        # create suggestion using wordlists
        suggestions[str(i)] = ""

    return json.dumps(suggestions)
