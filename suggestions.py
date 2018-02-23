import csv
import googlemaps
import json
import random
from datamuse import datamuse
from PyDictionary import PyDictionary

api = datamuse.Datamuse()
dictionary = PyDictionary()
gmaps = googlemaps.Client(open('google-api-key.txt', 'r').read())

reserved = []
with open('data/ReservedList.csv', 'r') as cs:
    reserved_temp = list(csv.reader(cs))[1:]
    for sublist in reserved_temp:
        for l in sublist:
            reserved.append(l)

registered = []
with open('data/20180222-zone-data.txt', 'r') as f:
    for line in f:
        registered.append(line.split(None, 1)[0])

# buying_prefixes = []
# selling_prefixes = []
cultural_data = json.load(open('data/cultural.json'))


def get_locations(location):
    locations = []
    address_raw = gmaps.reverse_geocode(location)
    for d in address_raw:
        if 'neighborhood' in d['types'] or 'locality' in d['types']:
            locations.append(d['address_components'][0]['long_name'].lower().replace(' ', ''))
    return locations


def get_tlds(tld_string):
    tlds = []
    if tld_string.split('autos:', 1)[1][:4] == 'true':
        tlds.append('.autos')
    if tld_string.split('boats:', 1)[1][:4] == 'true':
        tlds.append('.boats')
    if tld_string.split('homes:', 1)[1][:4] == 'true':
        tlds.append('.homes')
    if tld_string.split('motorcycles:', 1)[1][:4] == 'true':
        tlds.append('.motorcycles')
    if tld_string.split('yachts:', 1)[1][:4] == 'true':
        tlds.append('.yachts')
    return tlds


def get_adjectives(word):
    adj = api.words(rel_jjb=word, max=10)
    adjectives = []
    for a in adj:
        adjectives.append(a['word'])
    return adjectives


def get(customizer, tlds, location=0):
    locations = []
    if location != 0:
        locations = get_locations(location)
    customizer = customizer.lower()
    tlds = get_tlds(tlds)
    part_of_speech = list(dictionary.meaning(customizer).keys())[0]
    synonyms = dictionary.synonym(customizer)
    adjectives = get_adjectives(customizer)
    prefixes = []
    infixes = []
    suffixes = ['now']

    # if website_info['modifier'] == 'buying':
    #     prefixes += buying_prefixes
    # elif website_info['modifier'] == 'selling':
    #     prefixes += selling_prefixes

    prefixes += adjectives
    if part_of_speech == 'Noun':
        prefixes += locations
    else:
        suffixes += locations

    if len(locations) > 0 and locations[0] in cultural_data.keys():
        infixes += cultural_data[locations[0]]

    random.shuffle(prefixes)
    random.shuffle(suffixes)

    originals = {}
    suggestions = {}

    for t in tlds:
        domain = (customizer + t).lower()
        if domain in registered or domain in reserved:
            originals[domain] = False
        else:
            originals[domain] = True

    for i in range(min(10, len(prefixes))):
        for tld in tlds:
            domain = (prefixes[i] + customizer + tld).lower()
            if domain in registered or domain in reserved:
                suggestions[domain] = False
            else:
                suggestions[domain] = True

    for i in range(min(10, len(suffixes))):
        for tld in tlds:
            domain = (customizer + suffixes[i] + tld).lower()
            if domain in registered or domain in reserved:
                suggestions[domain] = False
            else:
                suggestions[domain] = True

    for infix in infixes:
        for tld in tlds:
            domain = (infix + tld).lower()
            if domain in registered or domain in reserved:
                suggestions[domain] = False
            else:
                suggestions[domain] = True

    for i in range(min(10, len(synonyms))):
        for tld in tlds:
            domain = (synonyms[i] + tld).lower()
            if domain in registered or domain in reserved:
                suggestions[domain] = False
            else:
                suggestions[domain] = True

    for i in range(min(3, len(synonyms))):
        for j in range(min(3, len(prefixes))):
            for tld in tlds:
                domain = (prefixes[j] + synonyms[i] + tld).lower()
                if domain in registered or domain in reserved:
                    suggestions[domain] = False
                else:
                    suggestions[domain] = True

    for i in range(min(3, len(synonyms))):
        for j in range(min(3, len(suffixes))):
            for tld in tlds:
                domain = (synonyms[i] + suffixes[j] + tld).lower()
                if domain in registered or domain in reserved:
                    suggestions[domain] = False
                else:
                    suggestions[domain] = True

    urls = {'originals': originals, 'suggestions': suggestions}
    return urls
