letterFrequencies = {"A": 9,"B": 2,"C": 2,"D": 4,"E": 12,"F": 2,"G": 3,"H": 2,"I": 9,"J": 1,"K": 1,"L": 4,"M": 2,"N": 6,"O": 8,"P": 2,"Q": 1,"R": 6,"S": 4,"T": 6,"U": 4,"V": 2,"W": 2,"X": 1,"Y": 2,"Z": 1,"_": 2}    
letterScores = {"A": 1,"B": 3,"C": 3,"D": 2,"E": 1,"F": 4,"G": 2,"H": 4,"I": 1,"J": 8,"K": 5,"L": 1,"M": 3,"N": 1,"O": 1,"P": 3,"Q": 10,"R": 1,"S": 1,"T": 1,"U": 1,"V": 4,"W": 4,"X": 8,"Y": 4,"Z": 10,"_": 0}
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"

def incrementDeckOrdered(predeck, deckSize):

    if len(predeck) == 0:
        return predeck

    lastCharacter = predeck[-1]
    indexOfNext = alphabet.find(lastCharacter) + 1

    placed = False
    while not placed:
        if indexOfNext >= len(alphabet):
            carriedDeck = incrementDeckOrdered(predeck[:-1], deckSize)
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


def NumberOfDecksOfSize(deckSize):
    startingDeck = "A" * deckSize
    progressDeck = startingDeck

    countedAll = False
    count = 0
    while not countedAll:
        progressDeck = incrementDeckOrdered(progressDeck, deckSize)
        count += 1
        if progressDeck == startingDeck:
            countedAll = True

    return count

totalCount = 0
for i in range(7):
    partialSum = NumberOfDecksOfSize(i+1)
    print(str(i+1)+ ": " + str(partialSum))
    totalCount += partialSum
print("Total: " + str(totalCount))
            




    


