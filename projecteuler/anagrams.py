from collections import defaultdict

class Anagrams:
    def __init__(self, wordsfile=r'C:\Users\j\Downloads\CSW12.txt')
        with open(wordsfile, encoding='utf-8') as f:
            words = [line.split(" ")[0] for line in f.readlines()]

        self.sortedcharmap = defaultdict(list)
        for word in words:
            self.sortedcharmap["".join(sorted(word))].append(word)
    def anagrams(self, word):
        key = "".join(sorted(word))
        if key in self.sortedcharmap:
            return self.sortedcharmap[key][:]
        return []
