import math, random, re
from collections import defaultdict, Counter
from bs4 import BeautifulSoup
import requests

def generate_using_bigrams(transitions):
    current = "."   # this means the next word will start a sentence
    result = []
    while True:
        next_word_candidates = transitions[current]    # bigrams (current, _)
        current = random.choice(next_word_candidates)  # choose one at random
        result.append(current)                         # append it to results
        if current == ".": return " ".join(result)     # if "." we're done

def generate_using_trigrams(starts, trigram_transitions):
    current = random.choice(starts)   # choose a random starting word
    prev = "."                        # and precede it with a '.'
    result = [current]
    while True:
        next_word_candidates = trigram_transitions[(prev, current)]
        next = random.choice(next_word_candidates)

        prev, current = current, next
        result.append(current)

        if current == ".":
            return " ".join(result)
            
def fix_unicode(text):
    return text.replace(u"\u2019", "'")

def get_document():

    url = "https://www.oreilly.com/ideas/use-deep-learning-on-data-you-already-have"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html5lib')

    content = soup.find("div", "article-body")        # find article-body div
    regex = r"[\w']+|[\.]"                            # matches a word or a period

    document = []


    for paragraph in content("p"):
        words = re.findall(regex, fix_unicode(paragraph.text))
        document.extend(words)

    return document
            
if __name__ == "__main__":

    document = get_document()

    bigrams = zip(document, document[1:])
    transitions = defaultdict(list)
    for prev, current in bigrams:
        transitions[prev].append(current)

    random.seed(0)
    print "bigram sentences"
    for i in range(10):
        print i, generate_using_bigrams(transitions)
    print

    # trigrams

    trigrams = zip(document, document[1:], document[2:])
    trigram_transitions = defaultdict(list)
    starts = []

    for prev, current, next in trigrams:

        if prev == ".":              # if the previous "word" was a period
            starts.append(current)   # then this is a start word

        trigram_transitions[(prev, current)].append(next)

    print "trigram sentences"
    for i in range(10):
        print i, generate_using_trigrams(starts, trigram_transitions)
    print