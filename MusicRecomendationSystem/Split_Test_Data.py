__author__ = 'Amin'
import math
"""
f - file object to open the file that contains the test data
fileVisible - file object to write to the visible part of test file
fileHidden - file object to write to the hidden part of test file
"""


f = open('Data/kaggle_visible_evaluation_triplets.txt', 'r')
fileVisible = open('kaggle_visible.txt', 'a')
fileHidden = open('kaggle_hidden.txt', 'a')
prev = ""
dat = []
count = 1
splitFactor = 0.5
for line in f:

    tokens = line.split()
    curr = tokens[0]
    if curr == prev:
        dat.append(line)

    else:

        prev = curr
        length = len(dat)
        if count != 1:
            split = math.ceil(splitFactor * length)
            split = int(split)
            firstPart = dat[0:split]
            secondPart = dat[split:length]
            dat = []
            dat.append(line)
            for obj in firstPart:
                fileVisible.write(obj)
            for obj in secondPart:
                fileHidden.write(obj)
        else:
            dat.append(line)
    count += 1

length = len(dat)
split = math.ceil(splitFactor * length)
split = int(split)
firstPart = dat[0:split]
secondPart = dat[split:length]
for obj in firstPart:
    fileVisible.write(obj)
for obj in secondPart:
    fileHidden.write(obj)




