import random
import time

words = []
with open("dictionary.txt") as file:
    words = file.read().split()

letterFrequencies = {"A": 9,"B": 2,"C": 2,"D": 4,"E": 12,"F": 2,"G": 3,"H": 2,"I": 9,"J": 1,"K": 1,"L": 4,"M": 2,"N": 6,"O": 8,"P": 2,"Q": 1,"R": 6,"S": 4,"T": 6,"U": 4,"V": 2,"W": 2,"X": 1,"Y": 2,"Z": 1,"_": 2}    
letterScores = {"A": 1,"B": 3,"C": 3,"D": 2,"E": 1,"F": 4,"G": 2,"H": 4,"I": 1,"J": 8,"K": 5,"L": 1,"M": 3,"N": 1,"O": 1,"P": 3,"Q": 10,"R": 1,"S": 1,"T": 1,"U": 1,"V": 4,"W": 4,"X": 8,"Y": 4,"Z": 10,"_": 0}
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"
deckSize = 7

def findWordsInDeck(deck):
    foundWords = []
    for word in words:
        d = deck.upper()
        valid = True
        if len(word) > len(deck):
            valid = False
        else:
            for character in word:
                if character in d:
                    cIndex = d.find(character)
                    d = d[:cIndex] + d[cIndex+1:]
                elif "_" in d:
                    cIndex = d.find("_")
                    d = d[:cIndex] + d[cIndex+1:]
                else:
                    valid = False
        if valid:
            foundWords.append(word)

    foundWords.sort(key=len,reverse=True)
    return foundWords

def incrementDeckOrdered(predeck):

    if len(predeck) == 0:
        return predeck

    lastCharacter = predeck[-1]
    indexOfNext = alphabet.find(lastCharacter) + 1

    placed = False
    while not placed:
        if indexOfNext >= len(alphabet):
            carriedDeck = incrementDeckOrdered(predeck[:-1])
            for c in alphabet:
                potentialDeck = carriedDeck + c
                if inOrder(potentialDeck) and potentialDeck.count(c) <= letterFrequencies[c]:
                    return potentialDeck
        else:
            newLastChar = alphabet[indexOfNext]
            potentialDeck = predeck[:-1] + newLastChar
            if inOrder(potentialDeck) and potentialDeck.count(newLastChar) <= letterFrequencies[newLastChar] and numberOfFollowers(potentialDeck) >= deckSize - len(potentialDeck):
                placed = True
                return potentialDeck
            else:
                indexOfNext += 1

def numberOfFollowers(deck):
    lastCharacter = deck[-1]
    lastCharIndex = alphabet.find(lastCharacter)
    count = 0
    for i in range(lastCharIndex, len(alphabet)):
        followingChar = alphabet[i]
        count += letterFrequencies[followingChar] - deck.count(followingChar)
    return count

def inOrder(deck):
    for i in range(1, len(deck)):
        if alphabet.find(deck[i]) < alphabet.find(deck[i-1]):
            return False
    return True

def generateDeck():
    bag = ""
    for c in alphabet:
        bag += c * letterFrequencies[c]
    deck = ""
    while len(deck) < 7:
        randomIndex = random.randrange(len(bag))
        deck += bag[randomIndex]
        bag = bag[:randomIndex] + bag[randomIndex+1:]
    return deck

####################################################################

def incrementDeck(predeck):
    if len(predeck) == 0:
        return predeck
    lastCharacter = predeck[-1]
    if lastCharacter == "_":
        return incrementDeck(predeck[:-1]) + "A"
    nextCharacter = alphabet[alphabet.find(lastCharacter) + 1]
    placed = False
    while not placed:
        if predeck.count(nextCharacter) + 1 <= letterFrequencies[nextCharacter]:
            postdeck = predeck[:-1] + nextCharacter
            placed = True
        else:
            if nextCharacter == "_":
                return incrementDeck(predeck[:-1]) + "A"
            nextCharacter = alphabet[alphabet.find(nextCharacter) + 1]
    return postdeck

def countStartingDecks(): #Pretty quick (<2 minutes)

    initialDeck = "AAAAAAA"
    finalDeck = "WXYYZ__"
    count = 1
    orderedCount = 1

    startTime = time.time()

    significantValues = [50,100,1000,2000,5000,10000]

   while initialDeck != finalDeck:
        initialDeck = incrementDeckOrdered(initialDeck)
        orderedCount += 1
        if orderedCount in significantValues or orderedCount % 100000 == 0:
            print (initialDeck + " : " + str(orderedCount))

    endTime = time.time()

    print("Final count is " + str(orderedCount) + "\n")
    print("Took " + str(endTime-startTime) + " seconds")

 
def findStartingWords(): #May take several days
    startingWords = set()
    foundWordsCount = 0
    count = 0
    startTime = time.time()
    with open("decks.txt") as file:
        decks = file.read().split("\n")
        for deck in decks:
            deckWords = findWordsInDeck(deck)
            for word in deckWords:
                startingWords.add(word)
            foundWordsCount += len(deckWords)
            count += 1
            if count % 100 == 0:
                print(deck + ": " + str(len(deckWords)) + " words found. " + str(len(startingWords)) + "/" + str(foundWordsCount) + " unique words found so far. " + str(count) + "/3325782 " + str(round(100 * (count/3325782.0), 2)) + "%")

    endTime = time.time()
    print("There are " + str(len(startingWords)) + " possible starting words.")
    print("Took " + str(endTime - startTime) + " seconds.")

    with open("Starting words.txt", "w") as file:
        wordList = list(startingWords)
        for word in wordList:
            file.write(word + "\n")

    print("All words written to file.")
