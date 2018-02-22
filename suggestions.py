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
            locations.append(d['address_components'][0]['long_name'])
    return locations


def get_tlds(tld_list):
    tlds = []
    if tld_list[0]:
        tlds.append('.autos')
    if tld_list[1]:
        tlds.append('.boats')
    if tld_list[2]:
        tlds.append('.homes')
    if tld_list[3]:
        tlds.append('motorcycles')
    if tld_list[4]:
        tlds.append('yachts')
    return tlds


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
    customizer = website_info['customizer'].lower().strip(' ')
    tlds = get_tlds(website_info['tlds'])
    part_of_speech = dictionary.meaning(customizer).keys()[0]
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

    if locations[0] in cultural_data.keys():
        infixes += cultural_data[locations[0]]

    prefixes = random.shuffle(prefixes)
    suffixes = random.shuffle(suffixes)

    originals = {}
    suggestions = {}

    for t in tlds:
        domain = customizer + t
        if domain in registered or domain in reserved:
            suggestions[domain] = False
        else:
            suggestions[domain] = True

    for i in range(min(10, len(prefixes))):
        for tld in tlds:
            domain = prefixes[i] + customizer + tld
            if domain in registered or domain in reserved:
                suggestions[domain] = False
            else:
                suggestions[domain] = True

    for i in range(min(10, len(suffixes))):
        for tld in tlds:
            domain = customizer + suffixes[i] + tld
            if domain in registered or domain in reserved:
                suggestions[domain] = False
            else:
                suggestions[domain] = True

    for infix in infixes:
        for tld in tlds:
            domain = infix + tld
            if domain in registered or domain in reserved:
                suggestions[domain] = False
            else:
                suggestions[domain] = True

    for i in range(min(10, len(synonyms))):
        for tld in tlds:
            domain = synonyms[i] + tld
            if domain in registered or domain in reserved:
                suggestions[domain] = False
            else:
                suggestions[domain] = True

    for i in range(min(3, len(synonyms))):
        for j in range(min(3, len(prefixes))):
            for tld in tlds:
                domain = prefixes[j] + synonyms[i] + tld
                if domain in registered or domain in reserved:
                    suggestions[domain] = False
                else:
                    suggestions[domain] = True

    for i in range(min(3, len(synonyms))):
        for j in range(min(3, len(suffixes))):
            for tld in tlds:
                domain = suffixes[j] + synonyms[i] + tld
                if domain in registered or domain in reserved:
                    suggestions[domain] = False
                else:
                    suggestions[domain] = True

    urls = {'originals': originals, 'suggestions': suggestions}
    return json.dumps(urls)
