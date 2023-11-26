#!/usr/bin/env python
# -*-coding:utf-8 -*
import sys
import re

def clean_word(word):
    # Utilizar expresión regular para eliminar números y caracteres especiales
    cleaned_word = re.sub(r'[^a-zA-Z]', '', word)
    return cleaned_word

current_word = None
current_count = 0
word = None

doc_count = {}

for line in sys.stdin:
    result = line.replace("\n", "").split('\t')

    if len(result) != 2:
        # Ignorar líneas mal formateadas
        continue

    word, doc = result

    # Limpiar la palabra
    word = clean_word(word)

    if not word:
        # Si después de la limpieza la palabra está vacía, ignorar la línea
        continue

    if word in doc_count.keys():
        if doc in doc_count[word].keys():
            doc_count[word][doc] += 1
        else:
            doc_count[word][doc] = 1
    else:
        doc_count[word] = {doc: 1}

print('Word\t[ (Document1, Count1), ... ]')
for key, counts in doc_count.items():
    value = ""
    for doc, count in counts.items():
        value += "({},{}) ".format(doc, count)
    print("{}\t{}".format(key, value))