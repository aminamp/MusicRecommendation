__author__ = 'Amin'

from collections import OrderedDict
import collections
import math


def cosine_similarity(v1, v2):
    dotp = 0
    s = 0.0

    l2 = v2.keys()

    for item in l2:
        if item in v1:
            dotp += float(v2.get(item)) * float(v1.get(item))

    for w in v1.values():
        w = float(w)
        s += w * w
    len1 = math.sqrt(s)

    s = 0.0
    for w in v2.values():
        w = float(w)
        s += w * w
    len2 = math.sqrt(s)

    return dotp / (len1 * len2)


userMap = {}
itemMap = collections.defaultdict(OrderedDict)
userItemMap = collections.defaultdict(dict)
userTestMap = collections.defaultdict(dict)

itemReverseMap = collections.defaultdict()
userTestReverseMap = collections.defaultdict()
trainFile = open('msd_train.txt', 'r')
testFile = open("msd_test_visible.txt", 'r')
fileOut = open('out_file.txt', 'a')

for line in trainFile:

    tokens = line.split()
    userName = tokens[0]
    itemName = tokens[1]
    numberOfUsers = len(userMap)
    numberOfItems = len(itemMap)

    if not userName in userMap:
        userMap[userName] = numberOfUsers + 1
        userValue = numberOfUsers + 1
    else:
        userValue = userMap.get(userName)

    if not itemName in itemMap:
        itemMap[itemName] = numberOfItems + 1
        itemValue = numberOfItems + 1
        itemReverseMap[numberOfItems+1] = itemName
    else:
        itemValue = itemMap.get(itemName)

    userItemMap[userValue][itemValue] = tokens[2]
print("Done1")
for line in testFile:
    tokens = line.split()
    userName = tokens[0]
    itemName = tokens[1]
    numberOfUsers = len(userMap)
    numberOfItems = len(itemMap)

    if not userName in userMap:
        userMap[userName] = numberOfUsers + 1
        userValue = numberOfUsers + 1
        userTestReverseMap[numberOfUsers + 1] = userName
    else:
        userValue = userMap.get(userName)

    if not itemName in itemMap:
        itemMap[itemName] = numberOfItems + 1
        itemValue = numberOfItems + 1
    else:
        itemValue = itemMap.get(itemName)

    userTestMap[userValue][itemValue] = tokens[2]
print("Done2")
cosineDistance = collections.defaultdict(dict)
for testUser in userTestMap.items():
    for trainUser in userItemMap.items():
        val = cosine_similarity(trainUser[1], testUser[1])
        cosineDistance[testUser[0]][trainUser[0]] = val
print("Done3")

lenCos = len(cosineDistance)

K = 3
nearestNeighbors = [[]]
for i in range(0, lenCos - 1, 1):
    topKUsers = sorted(cosineDistance.items()[i][1].items(), key=lambda t: float(t[1]), reverse=True)
    userID = [[]]
    for j in range(0, K, 1):
        userID.append(topKUsers[j][0])
    nearestNeighbors.append([cosineDistance.items()[i][0], userID[1:]])

N = 50
lenNearestNeighbor = len(nearestNeighbors)

for i in range(1, lenNearestNeighbor - 1, 1):
    currTestMap = userTestMap.get(nearestNeighbors[i][0])
    newSongs = collections.defaultdict()
    for j in range(0, K, 1):
        currUserMap = userItemMap.get(nearestNeighbors[i][1][j])
        for k, v in currUserMap.items():
            if not k in currTestMap:
                if not k in newSongs:
                    newSongs[k] = v
                else:
                    val = newSongs.get(k)
                    newVal = max(val, v)
                    newSongs[k] = newVal
    d = sorted(newSongs.items(), key=lambda t: int(t[1]), reverse=True)
    numElems = min(N, len(d))
    dnew = d[:numElems]
    recommendedItems = collections.OrderedDict(dnew)


    userName = userTestReverseMap.get(nearestNeighbors[i][0])
    itemNames = []
    for key in recommendedItems.keys():
        itemName = itemReverseMap.get(key)
        itemNames.append(itemName)
    print >>fileOut, userName, " ", itemNames


testFile.close()
trainFile.close()
fileOut.close()