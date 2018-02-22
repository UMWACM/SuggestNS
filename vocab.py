from vocabulary.vocabulary import Vocabulary as vb
import json
def get_synonyms(word):
    synonyms = json.loads(vb.synonym(word))
    return [d['text'] for d in synonyms]
