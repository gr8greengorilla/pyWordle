import math
#Compare every word with every other word

#take the highest average bit

#use it

#filter the list of words

#repeat


#Returns every word in the dict

def getDict():
    with open("wordledict.txt") as f:
        lines = f.readlines()[0].split(",")
    
    for i in range(0,len(lines)):
        lines[i] = lines[i][2:-1]
    
    return lines[1:-3]

def checkWord(guess, sample):
    sample = list(sample)
    output = [-1,-1,-1,-1,-1]

    

    for i in range(0, len(guess)):

        if (guess[i] in sample):
            output[i] = 0
            if (guess[i] == sample[i]):
                output[i] = 1
        
        """   for i in range(0, len(guess)):
        if guess[i] == sample[i]: # if its in the right place, return 1
            output[i] = 1
            sample[i] = "_"
    
    for i in range(0, len(guess)):
        if guess[i] in sample: #if its in any other place, return 0
            output[i] = 0
            if (guess[i] != sample[i]):
                sample[sample.index(guess[i])] = "_" """
    
    return output

def getBitSplit(dictonary, word, j = 0):
    word = list(word)
    diclength = len(dictonary)
    if (diclength > 1):
        dictonary = dictonary[::int(math.log2(len(dictonary)))]

    bits = 0
    for i in range(0,len(dictonary)):



        print("".join(word) + " " + str(i) + "/" + str(len(dictonary)) + "  " + str(j) + "/" + str(diclength), end="\r")

        remainersize = len(filterList(dictonary, word, checkWord(word, dictonary[i])))
        p = remainersize/len(dictonary)
        
        if p > 0:
            bits += -math.log2(p)#get bit of new dict/old dic lengths
        else:
            print(p)
            print(str(remainersize) + " / " + str(len(dictonary)))
            print(checkWord(word, dictonary[i]))
        
    
    return bits/len(dictonary)


def filterList(dictonary, word, score):
    output = []
    for i in range(0,len(dictonary)):
        remove = False
        check = dictonary[i]
        for j in range(0,len(word)):
            
            if score[j] == -1 and word[j] in check:
                remove = True
                break
            
            elif score[j] == 0:
                if not word[j] in check[:j] + check[j+1:]:
                    remove = True
                    break
            
            elif score[j] == 1 and word[j] != check[j]:
                remove = True
                break

        if (not remove):
            output.append(check)
    
    return output
            

dict = getDict()

word = "crane"
dict = filterList(dict, word, [-1,-1,0,-1,-1])

word = "zappy"
dict = filterList(dict, word, [-1,0,-1,-1,1])




topscores = []
words = []
for i in range(0,len(dict)):
    score = getBitSplit(dict, dict[i], i)
    topscores.append(score)
    words.append(dict[i])

topscores.sort(reverse = False)

print()
for i in range(0,len(words)):
    print(words[i] + ":\t" + str(topscores[i]))