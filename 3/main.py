#!/usr/bin/env python3
import re
from enum import Enum

class fxType(Enum):
    MUL = 0
    DO = 1
    DONT = 2

lines = []
functions = []
sum1 = 0
sum2 = 0

def readFile():
    global lines
    with open("input.txt") as f:
        lines = f.readlines()

def parseLine(line):
    fxes = ["".join(x) for x in re.findall(r"(mul\(\d{1,3},\d{1,3}\))|(don't\(\))|(do\(\))", line)]
    # breakpoint()
    for f in fxes:
        # print(f)
        # breakpoint()
        if(re.match(r"mul\(\d{1,3},\d{1,3}\)", f)):
            functions.append([f, fxType.MUL])
        elif(re.match(r"don't\(\)", f)):
            functions.append([f, fxType.DONT])
        elif(re.match(r"do\(\)", f)):
            functions.append([f, fxType.DO])


def mul1():
    global sum1
    for f in functions:
        if f[1] == fxType.MUL:
            # breakpoint()
            numbers = re.findall(r"\d+", f[0])
            # print(f)
            sum1 += int(numbers[0]) * int(numbers[1])

def mul2():
    global sum2
    do = True
    for f in functions:
        if f[1] == fxType.MUL and do:
            # breakpoint()
            numbers = re.findall(r"\d+", f[0])
            # print(f)
            sum2 += int(numbers[0]) * int(numbers[1])
        elif f[1] == fxType.DO:
            do = True
        else:
            do = False

if __name__=="__main__":
    readFile()
    for l in lines:
        parseLine(l)
    mul1()
    print("Part 1:", sum1)
    mul2()
    print("Part 2:", sum2)
