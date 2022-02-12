import math
import wordfreq
import wordle

def getDict():
    with open("wordledict.txt") as f:
        lines = f.readlines()[0].split(",")
    
    for i in range(0,len(lines)):
        lines[i] = lines[i][2:-1]
    
    return lines[1:-3]

def checkWord(guess, sample):
    sample = list(sample)
    output = [-1,-1,-1,-1,-1]
    guess = list(guess)
    '''for i in range(0, len(guess)):

        if (guess[i] in sample):
            output[i] = 0
            if (guess[i] == sample[i]):
                output[i] = 1'''

    for i in range(0, len(guess)):
        if guess[i] == sample[i]:
            output[i] = 1
            guess[i] = "_"
            sample[i] = "+"

    for i in range(0, len(guess)):

        if guess[i] in sample: #if its in any other place, return 0
            output[i] = 0
            sample[sample.index(guess[i])] = "?"

    return output

def getBitSplit(dictonary, word, logpower=2):
    diclength = len(dictonary)

    if (logpower != 1 and diclength > logpower):
        dictonary = dictonary[::int(math.log(diclength, logpower))]
    samplelen = len(dictonary)

    bits = 0
    for i in range(0,len(dictonary)):
        compare = checkWord(word, dictonary[i])
        remainersize = len(filterList(dictonary, word, compare))
        p = remainersize/samplelen

        bits += -math.log2(p)#get bit of new dict/old dic lengths
        
    
    return bits/samplelen

def filterList(dictonary, word, score):
    output = []


    for realword in dictonary:
        remove = False
        check = list(realword)

        for i in range(0,len(word)):

                if score[i] == 1:
                    if (word[i] == check[i]):
                        
                        check[i] = "_"
                    else:
                        remove = True
                        break
        

        if not remove:
            for i in range(0,len(word)):
                if score[i] == 0:
                    if word[i] in check[:i] + check[i+1:]:
                        check[check.index(word[i])] = "_"
                    else:
                        remove = True
                        break


        if not remove:
            for i in range(0,len(word)):
                if (score[i] == -1 and word[i] in check):
                    remove = True
                    break

        if not remove:
            output.append(realword)
    
    return output


def getStats(dict):
    dictlen = len(dict)

    freqs = [wordfreq.word_frequency(elem, "en") for elem in dict]
    mean = sum(freqs)/dictlen
    sd = (sum((elem - mean) ** 2 for elem in freqs)/dictlen) ** .5

    freqs = [(elem - mean)/sd for elem in freqs]

    return mean, sd

def manualHelper():
    dict = getDict()
    mean, sd = getStats(dict)

    while True:
        word = input("Enter your word: ")
        result = [0,0,0,0,0]
        for i in range(0,5):
            result[i] = int(input(str(i + 1) + ": "))
        
        dict = filterList(dict, word, result)

        
        dictlen = len(dict)
        

        words = []
        dictlen = len(dict)
        for i in range(0,dictlen):
            print(str(i) + "/" + str(dictlen) + "\t", end="\r")
            score = getBitSplit(dict, dict[i])
            freq = Sigmoid((wordfreq.word_frequency(dict[i], "en") - mean)/sd)
            score = score * freq

            words.append((dict[i], score))

        #Sort the scores.
        while (len(words) > 0):
            highestval = words[0]
            for i in range(0,len(words)):
                if (highestval[1] > words[i][1]):
                    highestval = words[i]
            words.remove(highestval)
            print(highestval[0] + ":\t" + str(highestval[1]))
                

        print(str(dictlen) + " Total Words.")
    
def getStartingScore(word):
    dict = getDict()
    bit = getBitSplit(dict, word)

    print("             ", end="\r")
    print(word + ":\t" + str(bit))

def Sigmoid(x):
    return 1/(1+math.e ** -x)


def practiceSolver(runs, speed=2):
    dict = getDict()
    mean, sd = getStats(dict)
    output = ""

    for i in range(0,runs):

        print("game " + str(i))
        dict = getDict()
        game = wordle.Game()

        highestval = ("crane", 0)
        results = game.takeGuess(highestval[0])
        
        while results[0] != -200:

            dict = filterList(dict, highestval[0], results)

            #Add all values to arrays and give them scores
            words = []
            dictlen = len(dict)
            for i in range(0,dictlen):
                print(str(i) + "/" + str(dictlen) + "\t", end="\r")
                score = getBitSplit(dict, dict[i], speed)
                if (game.numGuesses > 10): #was 2
                    freq = Sigmoid((wordfreq.word_frequency(dict[i], "en") - mean)/sd)
                    score = score * freq

                words.append((dict[i], score))

            #Sort the scores.
            if (len(words) > 0):
                highestval = words[0]
                for i in range(0,len(words)):
                    if (highestval[1] < words[i][1]):
                        highestval = words[i]


            results = game.takeGuess(highestval[0])
            if results == [1,1,1,1,1]:
                print("                                           ", end="\r")
                print(str(game.numGuesses) + "\t" + highestval[0] + "\t\t")
                output += str(game.numGuesses)
                break
            
        
        if results[0] == -200:
            print("Loss")
            output += "L"

    with open("stats.txt","w") as f:
        f.write(output) 
    
    losses = 0
    average = 0.0
    for elem in list(output):
        if elem == "L":
            losses += 1
        else:
            average += int(elem)
    average /= float(runs)
    print("There were " + str(losses) + " losses with an average of " + str(average))

practiceSolver(1000, 10)