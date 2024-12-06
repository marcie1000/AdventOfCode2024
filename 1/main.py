#!/usr/bin/env python3

leftList = []
rightList = []
similarities = {}

def readFile():
    global leftList
    global rightList
    lines = []
    with open("input.txt") as f:
        lines = [x.split() for x in f.readlines()]
    for line in lines:
        leftList.append(int(line[0]))
        rightList.append(int(line[1]))

def mySort(myList):
    for i in range(0, len(myList)):
        max_ = 0
        foundIndex = 0
        for j in range(0, len(myList) - i):
            if myList[j] > max_:
                foundIndex = j
                max_ = myList[j]
        myList = myList[0:len(myList)-i] + [max_] + myList[len(myList)-i:]
        myList.pop(foundIndex)
    return myList

def sumDistances():
    sum_ = 0
    for i in range(0, len(leftList)):
        if leftList[i] < rightList[i]:
            sum_ += rightList[i] - leftList[i]
        else:
            sum_ += leftList[i] - rightList[i]
    return sum_

def calcSimilarities():
    totalSum = 0
    beginSearch = 0
    for left in leftList:
        i = beginSearch
        stop = False
        count = 0
        while not stop and i < len(rightList):
            if left < rightList[i]:
                stop = True
            elif left == rightList[i]:
                count += 1
            else:
                beginSearch += 1
            i += 1
        totalSum += count * left
    return totalSum

if __name__ == "__main__":
    readFile()
    leftList = mySort(leftList)
    rightList = mySort(rightList)
    print("Part 1: sum of distances is", sumDistances())
    print("Part 2: answer is", calcSimilarities())
