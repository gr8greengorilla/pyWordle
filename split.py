
output = ""

with open('Dict.txt') as f:
    lines = f.readlines()

    for line in lines:
        if (len(line)==6):
            output = output + line

with open("5LetterDict.txt", "w") as f:
    f.write(output) #Have to get rid of the last newline

