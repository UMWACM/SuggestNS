from PyDictionary import PyDictionary

dictionary = PyDictionary()


def get_synonyms(word):
    return dictionary.synonym(word)


print(get_synonyms('fishing'))
