#!/usr/bin/env python3

from enum import Enum

debug = []
debug.append("----------")
debug.append("----------")
debug.append("----------")
debug.append("----------")
debug.append("----------")
debug.append("----------")
debug.append("----------")
debug.append("----------")
debug.append("----------")
debug.append("----------")

COLOR_NC="\x1b[0m" # No Color
COLOR_RED="\x1b[31m"

class DirX(Enum):
    W = 0
    MID = 1
    E = 2

class DirY(Enum):
    N = 0
    MID = 1
    S = 2

class Direction(Enum):
    NW = 0
    N  = 1
    NE = 2
    E  = 3
    SE = 4
    S  = 5
    SW = 6
    W  = 7
    end = 8
    @staticmethod
    def buildDirection(dirx: type(DirX), diry: type(DirY)):
        strdir = ""
        if diry.name != "MID":
            strdir += diry.name
        if dirx.name != "MID":
            strdir += dirx.name
        if strdir == "":
            return None
        return Direction[strdir]
    @staticmethod
    def splitDirection(direction):
        name = direction.name
        dirx = DirX.MID
        diry = DirY.MID
        for i in range(len(name)):
            if name[i] == 'N':
                diry = DirY.N
            elif name[i] == 'S':
                diry = DirY.S
            elif name[i] == 'E':
                dirx = DirX.E
            elif name[i] == 'W':
                dirx = DirX.W
        return dirx, diry
    @staticmethod
    def invert(txt):
        xincr = 0
        yincr = 0
        for t in range(len(txt)):
            if txt[t] == 'N':
                txt = txt[0:t] + 'S' + txt[t+1:-1]
                yincr = -2
            elif txt[t] == 'S':
                txt = txt[0:t] + 'N' + txt[t+1:-1]
                yincr = +2
            elif txt[t] == 'E':
                txt = txt[0:t] + 'W' + txt[t+1:-1]
                xincr = +2
            elif txt[t] == 'W':
                txt = txt[0:t] + 'E' + txt[t+1:-1]
                xincr = -2
        return txt, xincr, yincr


class Pattern:
    def __init__(self):
        self.dirct = Direction.NW
        self.xInitial = 0
        self.yInitial = 0
        self.ptrX = 0
        self.ptrY = 0
        self.foundLen = 1
    def lookForWord(self, word: str, lines: list, start: int):
        self.foundLen = start
        self.updatePtr()
        # if(self.xInitial == 5 and self.yInitial == 0):
        #     breakpoint()
        i = 0
        while i < len(word) and not self.isOutOfBounds(lines) and lines[self.ptrY][self.ptrX] == word[i]:
            self.foundLen += 1
            i += 1
            self.updatePtr()
            if self.foundLen == len(word) + start:
                self.foundLen = start
                return True
                # total += 1
                # while self.foundLen > 0:
                #     self.foundLen -= 1
                #     self.updatePtr()
                #     debug[self.ptrY] = debug[self.ptrY][0:self.ptrX] + lines[self.ptrY][self.ptrX] + debug[self.ptrY][self.ptrX + 1:]
                # for l in debug:
                #     print(l)
                # print("initialX:", self.xInitial, "; initialY:", self.yInitial)
                # breakpoint()
        self.foundLen = start
        return False
    def lookForWords(self, aword: str, lines: list):
        global total
        quitt = False
        word = aword
        while not quitt:
            if self.lookForWord(word, lines, 1):
                total += 1
            if self.dirct.value < Direction.end.value:
                self.dirct = Direction(self.dirct.value + 1)
                # breakpoint()
            else:
                quitt = True
    def updatePtr(self):
        dirx, diry = self.dirct.splitDirection(self.dirct)
        if dirx == DirX.W:
            self.ptrX = self.xInitial - self.foundLen
        elif dirx == DirX.E:
            self.ptrX = self.xInitial + self.foundLen
        else:
            self.ptrX = self.xInitial
        if diry == DirY.N:
            self.ptrY = self.yInitial - self.foundLen
        elif diry == DirY.S:
            self.ptrY = self.yInitial + self.foundLen
        else:
            self.ptrY = self.yInitial
    # returns True if out of bounds
    def isOutOfBounds(self, lines):
        if (self.ptrX < 0 or
            self.ptrY < 0 or
            self.ptrY >= len(lines) or
            self.ptrX >= len(lines[self.ptrY])):
            return True
        return False

class CrossPattern(Pattern):
    def __init__(self):
        self.dirct = Direction.NW
        self.originalDir = Direction.NW
        self.xInitial = 0
        self.yInitial = 0
        self.xInitial0 = 0
        self.yInitial0 = 0
        self.ptrX = 0
        self.ptrY = 0
        self.foundLen = 1
    def lookForCross(self, aword: str, lines: list):
        global debug
        global crossmatch
        global COLOR_NC
        global COLOR_RED
        quitt = False
        word = aword
        while not quitt:
            # if(self.xInitial == 7 and self.yInitial == 1):
            #     breakpoint()
            if self.lookForWord(word[1:], lines, 1):
                self.xInitial0 = self.xInitial
                self.yInitial0 = self.yInitial
                self.originalDir = self.dirct
                possibility = []
                dirx, diry = self.dirct.splitDirection(self.dirct)
                dirxInv, xincr, _ = Direction.invert(dirx.name)
                diryInv, _, yincr = Direction.invert(diry.name)
                possibility.append({'dir': Direction[diry.name + dirxInv] , 'x': self.xInitial + xincr, 'y': self.yInitial})
                possibility.append({'dir': Direction[diryInv + dirx.name] , 'x': self.xInitial, 'y': self.yInitial + yincr})

                amatch = False
                j = 0
                anciendebug = debug.copy()
                while not amatch and j < len(possibility):
                    self.xInitial = possibility[j]['x']
                    self.yInitial = possibility[j]['y']
                    self.dirct = possibility[j]['dir']
                    if self.lookForWord(word, lines, 0):
                        crossmatch += 1
                        amatch = True

                    #     while self.foundLen > 0:
                    #         self.foundLen -= 1
                    #         self.updatePtr()
                    #         debug[self.ptrY] = debug[self.ptrY][0:self.ptrX] + lines[self.ptrY][self.ptrX] + debug[self.ptrY][self.ptrX + 1:]
                    #         anciendebug[self.ptrY] = anciendebug[self.ptrY][0:self.ptrX] + '-' + anciendebug[self.ptrY][self.ptrX + 1:]
                        self.foundLen = 1
                    j += 1

                self.xInitial = self.xInitial0
                self.yInitial = self.yInitial0
                self.dirct = self.originalDir
                # if amatch:
                #     self.foundLen = 3

                #     while self.foundLen > 0:
                #         self.foundLen -= 1
                #         self.updatePtr()
                #         debug[self.ptrY] = debug[self.ptrY][0:self.ptrX] + lines[self.ptrY][self.ptrX] + debug[self.ptrY][self.ptrX + 1:]
                #         anciendebug[self.ptrY] = anciendebug[self.ptrY][0:self.ptrX] + '-' + anciendebug[self.ptrY][self.ptrX + 1:]
                #     self.foundLen = 1
                #     for l in range(len(debug)):
                #         for m in range(len(debug[l])):
                #             if debug[l][m] != anciendebug[l][m]:
                #                 print(COLOR_RED + debug[l][m] + COLOR_NC, sep="", end="")
                #             else:
                #                 print(debug[l][m], sep="", end="")
                #         print("")
                #     breakpoint()
            if self.dirct.value < Direction.W.value:
                self.dirct = Direction(self.dirct.value + 2)
                # breakpoint()
            else:
                quitt = True


class Lines:
    def __init__(self):
        self.l = []
        self.xCursor = 0
        self.yCursor = 0

    def lookForXMAS(self):
        for y in range(0, len(self.l)):
            for x in range(0, len(self.l[y])):
                if self.l[y][x] == "X":
                    amatch = Pattern()
                    amatch.xInitial = x
                    amatch.yInitial = y
                    # breakpoint()
                    amatch.lookForWords("MAS", self.l)

    def lookForMAS_cross(self):
        for y in range(0, len(self.l)):
            for x in range(0, len(self.l[y])):
                if self.l[y][x] == "M":
                    amatch = CrossPattern()
                    amatch.xInitial = x
                    amatch.yInitial = y
                    # breakpoint()
                    amatch.lookForCross("MAS", self.l)

ln = Lines()
global total
total = 0
global crossmatch
crossmatch = 0

def readFile():
    with open("input.txt") as f:
        ln.l = f.readlines()

if __name__=="__main__":
    # global ln
    readFile()
    ln.lookForXMAS()
    ln.lookForMAS_cross()
    # global total
    print("Part1: Number of XMAS:", total)
    print("Part2: Number of X-MAS:", int(crossmatch / 2))
    # for l in debug:
    #     print(l)
