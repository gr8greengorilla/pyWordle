import random

def randomWord():
    with open("5LetterDict.txt") as f:
        lines = f.readlines()
    
    return list(lines[random.randint(0,len(lines))])

def checkWord(guess, word):
    sample = word[:]
    output = [-1,-1,-1,-1,-1]
    for i in range(0, len(guess)):

        if guess[i] == word[i]: # if its in the right place, return 1
            output[i] = 1
        elif guess[i] in word: #if its in any other place, return 0
            output[i] = 0

        sample[i] = '_'
    
    return output

def makeGuess(guess, word): #returns True if won, and updates alphabet based on guess
    global correct
    global close
    global wrong
    global totalGuesses

    result = checkWord(guess, word)
    if result == [1,1,1,1,1]:
        return True
    
    for i in range(0, len(guess)):
        if result[i] == 1:
            correct.append(guess[i])
        elif result[i] == 0:
            close.append(guess[i])
        elif result[1] == -1:
            wrong.append(guess[i])
    
    totalGuesses.append((guess, result))

def printAlphabet():
    global correct
    global close
    global wrong

    alpha = list("abcdefghijklmnopqrstuvwxyz")

    output = []

    for letter in alpha:
        if letter in correct:
            output.append("*" + letter + "*")
        elif letter in close:
            output.append("~" + letter + "~")
        elif letter in wrong:
            pass
        else:
            output.append(letter)

    print((" ".join(output)).upper())

def printBoard():
    global totalGuesses
    global numGuesses

    output = []
    for entry in totalGuesses:
        

        for i in range(0,len(entry[0])):
            if (entry[1][i] == -1):
                output.append(" " + entry[0][i] + " ")
            elif (entry[1][i] == 0):
                output.append("~" + entry[0][i] + "~")
            elif (entry[1][i] == 1):
                output.append("*" + entry[0][i] + "*")
            
        output.append("\n")
    
    for i in range(0,numGuesses - len(totalGuesses)):
        output.append(" - - - - - - \n")
    
    print("".join(output))

def inDic(word):
    with open("5LetterDict.txt") as f:
        lines = f.readlines()
    return word + "\n" in lines

wrong = []
close = []
correct = []
totalGuesses = []
numGuesses = 6

secretWord = randomWord()

while (len(totalGuesses) < numGuesses):
    a = input("Make a guess\n")

    if (inDic(a)):
        if makeGuess(list(a), secretWord):
            print("You win!")
            exit()
        else:
            print("\n\n")
            printBoard()
            print("\n")
            printAlphabet()

print("You lose")
print("Word was " + "".join(secretWord))