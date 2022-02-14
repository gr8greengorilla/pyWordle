from http import cookies
import math
from re import S
from statistics import variance
import wordfreq
import wordle
import multiprocessing
from functools import partial

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

def manualHelper(speed=2, cores=1):
    dict = getDict()
    mean, sd = getStats(dict)

    guessnum = 0
    while True:
        word = input("Enter your word: ")
        result = [0,0,0,0,0]
        for i in range(0,5):
            result[i] = int(input(str(i + 1) + ": "))
        
        dict = filterList(dict, word, result)

        
        dictlen = len(dict)
        

        #Give all values a score
        words = dict.copy()
        if (cores > 1 and len(dict) > 500):
            words = getScoresMulticore(guessnum, words, speed, (mean, sd), cores)
        else:
            words = getScores(guessnum, words, speed, (mean,sd))

        #Sort the scores.
        while (len(words) > 0):
            highestval = words[0]
            for i in range(0,len(words)):
                if (highestval[1] > words[i][1]):
                    highestval = words[i]
            words.remove(highestval)
            print(highestval[0] + ":\t" + str(highestval[1]))
                

        print(str(dictlen) + " Total Words.")
        guessnum += 1
    
def getStartingScore(word, speed):
    dict = getDict()
    bit = getBitSplit(dict, word, speed)

    print("             ", end="\r")
    print(word + ":\t" + str(bit))


def Sigmoid(x):
    return 1/(1+math.e ** -x)


def getScores(numguesses, dict, speed, stats):
    words = []
    for i, word in enumerate(dict):
        #print(str(i) + "/" + str(dictlen) + "\t", end="\r")
        score = getBitSplit(dict, word, speed)
        
        #if numguesses > 2:
        #freq = Sigmoid((wordfreq.word_frequency(word, "en") - stats[0])/stats[1])
        #score = score * freq

        words.append((word, score))
    
    return words


def getScoreMulticore2(guessnum, speed, stats, dict, word):
    score = getBitSplit(dict, word, speed)

    if guessnum > 2:
            #freq = Sigmoid((wordfreq.word_frequency(word, "en") - stats[0])/stats[1])
            freq = (wordfreq.word_frequency(word, "en") - stats[0])/stats[1]
            score = score * freq

    return (word, score)
    

def getScoresMulticore(guessnum, dict, speed, stats, cores=1):
    
    temp = partial(getScoreMulticore2, guessnum, speed, stats, dict)
    print(len(dict), end="          \r")
    with multiprocessing.Pool(cores) as pool:
        result = pool.map(func=temp, iterable=dict)
    return result

def runGame(dict, speed, stats, _):

    game = wordle.Game()

    highestval = ("crane", 0)
    results = game.takeGuess(highestval[0])
    
    while results[0] != -200:

        dict = filterList(dict, highestval[0], results)

        #Give all values a score
        words = dict.copy()
        words = getScores(game.numGuesses, words, speed, stats)

        #Sort the scores.
        if (len(words) > 0):
            highestval = words[0]
            for i in range(0,len(words)):
                if (highestval[1] < words[i][1]):
                    highestval = words[i]


        results = game.takeGuess(highestval[0])
        if results == [1,1,1,1,1]:
            return game.numGuesses, highestval[0]
    return (-1, "".join(game.secretWord))


def practiceSolver(amount, dict, speed, multiprocess=False, verbose=True):
    stats = getStats(dict)
    temp = partial(runGame, dict, speed, stats)
    output = []
    if (multiprocess):
        with multiprocessing.Pool() as pool:
            for i, result in enumerate(pool.imap_unordered(func=temp, iterable=[0] * amount), 1):
                print(f"\r{(i/amount) * 100:.2f}%", end="\r")
                output.append(result)
    else:
        for i in range(0,amount):
            output.append(runGame(dict, speed, stats, 0))
            print(f"\r{(i/amount) * 100}%", end="\r")

    if verbose:
        data = [i for i, _ in output if i != -1]
        mean = sum(data)/len(data)
        sd = (sum((i - mean) ** 2 for i in data)/len(data)) ** .5

        print(f"After {amount} trails with a speed of {speed}, there was a mean of {mean:.5f} guesses with a SD of {sd:.3f}. Fails: {len(output) - len(data)}")
    return output



#C:\Users\erik\OneDrive\Cross-Code\VSCode\PythonCode\Javascript\Wordle
def main():
    practiceSolver(1000,getDict(),2, multiprocess=True, verbose=True)

if __name__ == '__main__':
    main()