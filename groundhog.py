#!/usr/bin/python3

import sys
from math import pow, sqrt

ts = []

bollinger = [0.0, 0.0]
weirdest = [0.0, 0.0, 0.0, 0.0, 0.0]
weirdRatio = [0.0, 0.0, 0.0, 0.0, 0.0]
period = 0 ; switches = 0 ; lastRelative = 0.0

def getTIA():
    avg = 0.0
    print("g=", end='')
    try:
        for n in range(1, period + 1):
            if (ts[-n] > ts[-(n + 1)]):
                avg += ts[-n] - ts[-(n + 1)]
        print("%.2f" % (avg / period), end='')
    except:
        print("nan", end='')


def getRTE():
    global lastRelative

    print("\tr=", end='')
    try:
        start = 0.0; s = False
        for idx in range(-(period + 1), 0):
            if (ts[idx] != 0.0): start = ts[idx] ; break
        act = round(100 * ((ts[-1] - start) / abs(start)))
        print("%d%%" % act, end='')
        if (act * lastRelative < 0): s = True
        lastRelative = act
        return (s)
    except:
        print("nan%", end='')
        return False


def getSDev():
    global bollinger
    esp = 0.0 ; var = 0.0

    print("\ts=", end='')
    try:
        for n in range(1, period + 1):
            esp += ts[-n]
        esp /= period
        for n in range(1, period + 1):
            var += pow((ts[-n] - esp), 2)
        var = sqrt(var / period)
        print("%.2f" % var, end='')
        bollinger = [esp - (3 * var), esp + (3 * var)]
    except:
        print("nan", end='')


def replaceWeirdestValue(newDist):
    n = 0
    while (weirdRatio[n] != min(weirdRatio)):
        n += 1
    while (n < 4):
        weirdRatio[n] = weirdRatio[n + 1]
        weirdest[n] = weirdest[n + 1]
        n += 1
    weirdRatio[n] = newDist
    weirdest[n] = ts[-1]


def checkWeirdest():
    if (len(ts) <= period + 1 or (ts[-1] >= bollinger[0] and ts[-1] <= bollinger[1])):
        return
    oddDiff = (bollinger[0] - ts[-1]) if (ts[-1] < bollinger[0]) else (ts[-1] - bollinger[1])
    if (min(weirdRatio) < oddDiff):
        replaceWeirdestValue(oddDiff)


def SortWeirdValues():
    global weirdest
    newList = [
        [weirdest[0], weirdRatio[0]],
        [weirdest[1], weirdRatio[1]],
        [weirdest[2], weirdRatio[2]],
        [weirdest[3], weirdRatio[3]],
        [weirdest[4], weirdRatio[4]]
    ]
    l = len(newList)
    for i in range(0, l):
        for j in range(0, l-i-1):
            if (newList[j][1] > newList[j + 1][1]):
                tmp = newList[j]
                newList[j] = newList[j + 1]
                newList[j + 1] = tmp
    newList.reverse()
    weirdest = [
        newList[0][0],
        newList[1][0],
        newList[2][0],
        newList[3][0],
        newList[4][0]
    ]
    return weirdest


def groundHog():
    global switches
    hasSwitched = False

    while True:
        tmp = input()
        if (tmp == "STOP"):
            break
        ts.append(float(tmp))
        checkWeirdest()
        getTIA()
        hasSwitched = getRTE()
        getSDev()
        if (hasSwitched):
            print("\ta switch occurs", end='')
            switches += 1
        print()


try:
    if (len(sys.argv) != 2):
        exit(84)
    period = int(sys.argv[1])
    groundHog()
    print("Global tendency switched %d times" % switches)
    print("5 weirdest values are", SortWeirdValues())
except:
    exit(84)