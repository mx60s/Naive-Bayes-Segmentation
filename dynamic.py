import numpy as np
import functools
import math

# Jane Austin's Pride and Prejudice
# TODO: figure out how to make urllib.request work correctly in python 3.6
with open('prideandprejudice.txt') as f:
    text = f.read()

# This text indicates italics with the use of underscores
d = {'.':'', ',':'', '?':'', '!':'', '-':'', ':':'', ';':'', '\"':'', '_':''}
trans = text.maketrans(d)
text = text.translate(trans)

chapters = []
while(text.rfind('CHAPTER')):
    i = text.rfind('CHAPTER')
    chapter = text[i:]
    chapter = chapter.lower()
    text = text[:i]
    chapters.append(chapter)
chapters.append(text)
chapters.reverse()

grams = dict()

for i in range(0,len(chapters)):
    words = chapters[i].split()
    for word in words:
        if not word in grams:
            grams[word] = 1
        else:
            grams[word] += 1

with open('grams.txt', 'w') as f:
    for word in grams:
        line = (word, str(grams[word]))
        sline = '\t'.join(line)
        f.write(sline)
        f.write('\n')
        #print(sline)

def splitPairs(line):
    return [(line[:i+1], line[i+1:]) for i in range(len(line))]


class OneGramBayes(dict):
    def __init__(self):
        self.gramCount = 0
        for line in open('grams.txt'):
            (word, count) = line[:-1].split('\t')
            self[word] = int(count)
            self.gramCount += self[word]
    def __call__(self,word):
        if word in self:
            return float(self[word])/self.gramCount
        else:
            return 1.0/(self.gramCount * 10**(len(word) - 2))

single_word_prob = OneGramBayes()

def wordSeqFitness(words):
    return functools.reduce(lambda x,y: x+y,
     (math.log10(single_word_prob(w)) for w in words))

def segment(word):
    if not word: return []
    allSegmentations = [[first]+ segment(rest) for (first,rest) in splitPairs(word)]
    #print(allSegmentations)
    return max(allSegmentations, key = wordSeqFitness)
    # assuming there is a global function wordSeqFitness which computes
    # the fitness of a given sequence of words, with respect to whether or
    # not it's probably the correct segmentation.

    # naive Bayes taking probabilities of each word and multiplying

print(segment('mustindeedgo'))