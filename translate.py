from loop import num_items_per_loop, four_at_a_time, three_at_a_time, two_at_a_time

import sys

'''
Two rings to find them
One ring to find them all
One ring to find him
One ring to find her
One ring to find it
One ring to find darkness
One ring to find in the darkness
One ring to find cake
One ring to find one ring
One ring to find
One ring to find one ring and two rings to find two rings

You need one ring to find them
I need one ring to find them
'''

"""
You need one ring to find them
bolk ash nazg gimbatul
"""

"""
I need one ring to find them
bolk ash nazg gimbatul
"""

numbers = [
    'ash',
    'krul',
]

def split_line(line):
    first, second, third = line.split(',')
    return {
        'english': first,
        'black_speech': second,
        'type': third,
    }

def build_dic():
    with open('BlackSpeech.txt', encoding='latin') as f:
        text = f.read()

    return [
        split_line(line)
        for line in text.splitlines()
    ]

dic = [
    {
        'english': 'the',
        'black_speech': '',
        'type': 'ignore',
    },
] + build_dic()

dic_eng_key = {
    d['english']: d
    for d in dic
}

# 'to' + 'verb' = '-at'
# subject verb object

def make_proper(words):
    for first, second, third in three_at_a_time(words):
        yield first

        if first['type'] != 'preposition' and second['type'] == 'verb' and third['type'] in ('noun', 'pronoun'):
            yield dic_eng_key['to']

def prepose_verbs(words, next_word=None):
    try:
        first = next(words) if next_word is None else next_word
    except StopIteration:
        return

    try:
        second = next(words)
    except StopIteration:
        yield first
        return

    if first['type'] == 'preposition' and first['english'] == 'to' and second['type'] == 'verb':
        yield {
            'english': first['english'] + ' ' + second['english'],
            'black_speech': second['black_speech'] + 'at',
            'types': ('preposition', 'verb'),
            'type': 'prepositioned_verb',
        }
        for item in prepose_verbs(words, next_word=None):
            yield item
    else:
        yield first
        for item in prepose_verbs(words, next_word=second):
            yield item

def prepose_nouns(words, next_word=None):
    try:
        first = next(words) if next_word is None else next_word
    except StopIteration:
        return

    try:
        second = next(words)
    except StopIteration:
        yield first
        return

    if first['type'] == 'preposition' and second['type'] == 'noun':
        yield second
        yield first
        for item in prepose_nouns(words, next_word=None):
            yield item
    else:
        yield first
        for item in prepose_nouns(words, next_word=second):
            yield item

def ignore(words):
    return (word for word in words if word['type'] != 'ignore')

def translate_sentence(sentence):
    meta_sentence = (
        dic_eng_key[word.lower()]
        for word in sentence.split()
    )

    proper_english_sentence = make_proper(meta_sentence)

    ruled_sentence = tuple(prepose_verbs(prepose_nouns(ignore(proper_english_sentence))))


    return sentence + ' = ' + ' '.join(
        d['black_speech'] for d in ruled_sentence)

if __name__ == '__main__':
    try:
        user_input = sys.argv[1]
    except IndexError:
        user_input = None

    if user_input:
        print(translate_sentence(user_input))
    else:
        for sentence in ('one ring to rule them all', 'one ring to find them', 'one ring to bring them all', 'And in the darkness bind them'):
            """
            Ash nazg durbatuluk
            Ash nazg gimbatul
            Ash nazg thrakatuluk
            Agh burzum-ishi krimpatul
            """
            print(translate_sentence(sentence))
