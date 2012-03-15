#! /usr/bin/python
""" This program generates random text.

It expects a text file and generates simple statistics about likely
characters to follow a given character.  It then uses these statistics
to iteratively generate random text.

For this program to work, you must provide one or more source files:

    ./random-training-data/*.txt

The one optional argument is the number of random characters to generate,
which defaults to 1000.
"""

import sys, os, random, pprint, time
from collections import defaultdict

subdir = r'd:\books'
sourcefiles = [os.path.join('.', subdir, f) for f in os.listdir(subdir) if f[-3:]=='txt']

class TrigramDist:
    def __init__(self):
        self.chrs = set([chr(a) for a in range(ord('a'), ord('z')+1)] #a-z
                     +  [chr(a) for a in range(ord('A'), ord('Z')+1)] #A-Z
                     +  [' ', '.', ',', "'", '?', '\n']
                    )
        # build a structure to store probabilities:
        #     probabilities[prev][a]
        # is a number indicating how many times a followed prev in the source document
        self.probabilities = {a+b: defaultdict(int)
                              for a in self.chrs for b in self.chrs}
    def learnFromFile(self, sourceFilePath):
        # read in probabilities
        with open(sourceFilePath, 'r', encoding='latin-1') as sourceFile:
            prev = '  '
            for c in sourceFile.read():
                if c in self.chrs:
                    self.probabilities[prev][c] += 1
                    prev = prev[1:]+c
        # Work out the total number of choices for each letter (used in
        # probability calculation in select())
        self.totals = {a: 0 for a in self.probabilities.keys()}
        for prev, probs in self.probabilities.items():
            self.totals[prev] = sum(probs.values())
        if self.totals['. '] > self.totals['  ']:
            self.default = '. '
        else:
            self.default = '  '
    def select(self,prev):
        """Given a preceding string, randomly select the next character.
        Choose a letter based on
        the source document - for example, in English it is quite likely
        that 'q' will be followed by 'u', and this is reflected in the
        probabilities.  Thus this function will usually return 'u'
        when given 'q' and a set of probabilities generated from English text."""
        prev = prev[-2:]
        index = random.randint(0, self.totals[prev])
        for newletter, chance in self.probabilities[prev].items():
            index -= chance
            if index <= 0:
                return newletter

ngramProbs = TrigramDist()
t = time.time()
for fname in sourcefiles:
    print("learning from ", fname)
    ngramProbs.learnFromFile(fname)
print("done learning. Time: {}s".format(time.time()-t))
def makedoc(length, start=ngramProbs.default):
    """Generate a sequence of random characters."""
    prev = start
    doc = ""
    while length > 0:        
        prev = prev[1:]+ngramProbs.select(prev)
        doc += prev[-1] 
        length -= 1
    return doc

def streamChars(): 
    """Continuously stream random characters to stdout."""
    next = ngramProbs.default
    stepSize = 1
    while True:
        time.sleep(0.02)
        next = next[1:]+makedoc(stepSize, next[-2:])
        sys.stdout.write(next[-1])
        sys.stdout.flush()
        
if __name__ == "__main__":
    streamChars()
