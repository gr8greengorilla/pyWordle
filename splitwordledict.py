
output = ""

with open('wordledict.txt') as f:
    lines = f.readlines()

    words = lines[1].split(",")

    output += words[0][3:-1] + ","
    for i in range(1,len(words)-1):
        output += words[i][2:-1] + ","
    output += words[len(words)-1][2:-3]

with open("guessDict.txt", "w") as f:
    f.write(output) #Have to get rid of the last newline

