#!/usr/bin/env python3
from enum import Enum

class Dir(Enum):
    ASC = 0,
    DESC = 1,
    UNKNOWN = 3

reports = []

def readFile():
    global reports
    with open("input.txt") as f:
        reports = [[int(y) for y in x.split()] for x in f.readlines()]
        # reports = [int(x) for x in reports]

def isSafe(report):
    safe = True
    i = 0
    direction = Dir.UNKNOWN
    # breakpoint()
    while safe and i < len(report) - 1:
        if report[i] < report[i + 1] and (direction == Dir.UNKNOWN or direction == Dir.ASC):
            direction = Dir.ASC
        elif report[i] > report[i + 1] and (direction == Dir.UNKNOWN or direction == Dir.DESC):
            direction = Dir.DESC
        else:
            safe = False
        if abs(report[i] - report[i+1]) == 0 or abs(report[i] - report[i+1]) > 3:
            safe = False
        i += 1
    return safe

def isSafe2(report):
    # Counting and memorizing bad levels indexes
    i = 0
    direction = Dir.UNKNOWN
    removed=0
    directions = [] # memorize ASC/DESC/same compared to the next level
    ascending = 0 # counting ascendings
    descending = 0 # counting descendings
    same = 0 # counting sames
    upperto3 = 0 # counting when difference > 3
    upperto3index = 0 # memorizing index for this
    while i < len(report) - 1:
        if report[i] < report[i + 1]:
            ascending += 1
            directions.append(Dir.ASC)
        elif report[i] > report[i + 1]:
            descending += 1
            directions.append(Dir.DESC)
        else:
            same += 1
            directions.append(Dir.UNKNOWN)
        if abs(report[i] - report[i+1]) > 3:
            upperto3 += 1
            upperto3index = i # if there's more than one we will lose previous indexes
            # but it's okay because we won't test to remove those levels/indexes if there's
            # more than one anyway
        i += 1

    toDelete = [] # memorize indexes that we will remove for testing if it works
    # looks if asc / desc sheme is correct
    goodDirection = False
    if(ascending == 0 and descending != 0 and descending == len(report)) or (ascending != 0 and descending == 0 and descending == len(report)):
        goodDirection = True

    # looks if differences are correct
    goodDifferences = False
    if same == 0 and upperto3 == 0:
        goodDifferences = True

    # if both are correct we stop here
    if goodDifferences and goodDirection:
        return True

    # else...
    # if there's only one ascending and the others are descending, maybe removing
    # this index level would make the report correct, so we keep it in memory in
    # order to test it
    if ascending == 1:
        toDelete.append(directions.index(Dir.ASC))
    # same but vice versa
    elif descending == 1:
        toDelete.append(directions.index(Dir.DESC))
    # same but if there's only one level that is the same as the following one
    if same == 1:
        toDelete.append(directions.index(Dir.UNKNOWN))
    # same but with differences > 3
    if upperto3 == 1:
        toDelete.append(upperto3index)
    # if none of these 4 scenarios applies, toDelete will contain no element

    # try removing the faulty levels indexes, one by one, independantly
    for d in toDelete:
        i = d
        # we test deleting the index and also the following one (if exists),
        # because (I think) sometimes removing the following one can work
        while i < len(report) and i <= d + 1:
            r = report.copy()
            r.pop(i)
            # test with Part 1 function
            if isSafe(r):
                return True
            i += 1
    return False

def tests():
    assert(isSafe([5,4,3,2,1,0]))
    assert(isSafe([0,1,2,3,4,5]))
    assert(isSafe([10,8,6,4]))
    assert(isSafe([4,6,8,10]))
    assert(isSafe([1,0]))
    assert(isSafe([0,1]))
    assert(isSafe([0,3,6,9,12]))
    assert(isSafe([12,9,6,3,0]))
    assert(isSafe([100,102,103,106]))
    assert(isSafe([100, 98, 97, 96]))
    assert(not isSafe([1,0,0]))
    assert(not isSafe([1,1,0]))
    assert(not isSafe([1,10]))
    assert(not isSafe([10,1]))
    assert(not isSafe([1,1,1,1,1]))
    assert(not isSafe([1,0,1]))
    assert(not isSafe([10,11,12,13,12]))

if __name__ == "__main__":
    readFile()
    mySum = 0
    for report in reports:
        if(isSafe(report)):
            mySum += 1
    print("Part 1: the result is", mySum)
    for report in reports:
        if(isSafe2(report)):
            mySum += 1
    print("Part 1: the result is", mySum)
