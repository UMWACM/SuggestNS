import csv
import googlemaps
import json
from datamuse import datamuse
from PyDictionary import PyDictionary

api = datamuse.Datamuse()
dictionary = PyDictionary()
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

buying_prefixes = []
selling_prefixes = []
cultural_data = {'Norfolk': [], 'New York': [], 'Nashville': [], 'Rome': [], 'London': []}


def get_locations(location):
    locations = []
    address_raw = gmaps.reverse_geocode(location)
    for d in address_raw:
        if 'neighborhood' in d['types'] or 'locality' in d['types']:
            locations.append(d['address_components'][0]['long_name'])
    return locations


def get_adjectives(word):
    adj = api.words(rel_jjb=word, max=10)
    adjectives = []
    for a in adj:
        adjectives.append(a['word'])
    return adjectives


def get(website_json):
    website_info = json.loads(website_json)
    locations = []
    if len(website_info['location']) > 0:
        location = str(website_info['location']['lat']) + ',' + str(website_info['location']['long'])
        locations = get_locations(location)
    customizer = website_info['customizer']
    part_of_speech = dictionary.meaning(customizer).keys()[0]
    synonyms = dictionary.synonym(customizer)
    adjectives = get_adjectives(customizer)
    prefixes = []
    infixes = synonyms
    suffixes = ['now']

    if website_info['modifier'] == 'buying':
        prefixes += buying_prefixes
    elif website_info['modifier'] == 'selling':
        prefixes += selling_prefixes

    prefixes += adjectives
    if part_of_speech == 'Noun':
        prefixes += locations
        if locations[0] in cultural_data.keys():
            prefixes += cultural_data[locations[0]]
    else:
        suffixes += locations
        if locations[0] in cultural_data.keys():
            suffixes += cultural_data[locations[0]]

    suggestions = {}

    # range toggling depending on length of lists, using more infixes if other lists short, etc.
    for i in range(0, 100):
        # create suggestion using wordlists
        domain = ''

        if domain in registered or domain in reserved:
            suggestions[domain] = False
        else:
            suggestions[domain] = True

    return json.dumps(suggestions)
