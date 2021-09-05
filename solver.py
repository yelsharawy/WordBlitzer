from collections import Counter
from functools import reduce
import time
import pyautogui
import numpy as np

values = { line[0]:int(line[2:]) for line in open("scrabble_letters.txt").read().splitlines()}

game = ["GNYP", "EBOR", "SLEN", "UICE"]
lMult = np.ones((4,4),dtype='uint8')#[[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]]
wMult = np.ones((4,4),dtype='uint8')
lenScores = {2:3, 3:4, 4:6, 5:9, 6:11, 7:14, 8:15, 9:19, 10:22}
for i in range(8,17): # guesswork, will be replaced if possible
    lenScores[i] = 2 * i + 2

def charInGame(char):
    return char in game[0] \
           or char in game[1] \
           or char in game[2] \
           or char in game[3]
def stringInGame(string):
    return all(charInGame(c) for c in string)

def countChar(char):
    return game[0].count(char) + \
           game[1].count(char) + \
           game[2].count(char) + \
           game[3].count(char)

def enoughChars(string):
    return all(n <= countChar(c) for c, n in Counter(string).items())

def value(string):
    return sum(values[char] for char in string) + lenScores[len(string)]

def valueChain(chain):
    return sum(values[game[y][x]] * lMult[y][x] for y, x in chain)\
           * reduce(lambda x, y: x * y, (wMult[y][x] for y, x in chain))\
           + lenScores[len(chain)]

infile = open("scrabble_words2.txt")
# not up to date, but is what Word Blitz uses supposedly
lines = [line
         for line in infile.read().splitlines()
         if len(line) <= 16]

#realStart = time.perf_counter()
sort = lines # [x for x in lines if enoughChars(x)]
# print(time.perf_counter() - realStart)
def adj(t):
    y, x = t
    if y > 0:
        if x > 0:
            yield y - 1, x - 1
        yield y - 1, x
        if x < 3:
            yield y - 1, x + 1
    if x > 0:
        yield y, x - 1
    if x < 3:
        yield y, x + 1
    if y < 3:
        if x > 0:
            yield y + 1, x - 1
        yield y + 1, x 
        if x < 3:
            yield y + 1, x + 1
canMake = {}
count = 0
def tryString(string, chain, words=sort):
    global count
    if string in words:
        if string not in canMake:
            #print(string)
            canMake[string] = (valueChain(chain), chain)
            count += 1
        else:
            v = valueChain(chain)
            if v > canMake[string][0]:
                canMake[string] = (v, chain)

def tryAll(pos, chain=[], string="", words=sort, count=0):
    chain = chain.copy()
    chain.append(pos)
    char = game[pos[0]][pos[1]]
    string += char
    words = [x for x in words if x[count:count+1] == char]
    if len(words) == 0:
        return
    tryString(string, chain, words)
    possibleNext = (x for x in adj(chain[-1]) if x not in chain)
    for new in possibleNext:
        tryAll(new, chain, string, words, count + 1)

def tryEveryTile():
    global canMake
    global count
    canMake = {}
    count = 0
    for y in range(4):
        for x in range(4):
            tryAll((y, x))

def sortCanMake():
    return sorted(canMake, key=lambda k: canMake[k][0], reverse=True)
#tryAll((0,0))
# corners = 1012520
# edges =   740111
# center =  514668
if __name__ == '__main__':
    start = time.perf_counter()
    tryEveryTile()
    end = time.perf_counter()
    print(end - start)
    for word in sortCanMake():
        print(word, canMake[word])
    print(sum(canMake[string][0] for string in canMake))
