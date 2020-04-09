#!/usr/bin/python3

import sys
from math import pow, sqrt

ts = []
weirdRatio = []

bollinger = [0.0, 0.0]
weirdest = [0.0, 0.0, 0.0, 0.0, 0.0]
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
        return


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
        if (act != 0):
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
        bollinger = [esp - (2 * var), esp + (2 * var)]
    except:
        print("nan", end='')
        return


def storeWeirdRatio():
    if (len(ts) <= period + 1):
        oddDiff = 987654321.0
    elif (abs(bollinger[0] - ts[-2]) < abs(bollinger[1] - ts[-2])):
        oddDiff = abs(bollinger[0] - ts[-2])
    else:
        oddDiff = abs(bollinger[1] - ts[-2])
    # print("Value = [%.1f], Oddvalue = [%.3f]" % (ts[-1], oddDiff))
    weirdRatio.append(oddDiff)


def getOutliers():
    global weirdest
    
    for i in range(0, 5):
        idx = weirdRatio.index(min(weirdRatio))
        weirdest[i] = ts[idx - 1]
        weirdRatio.pop(idx)
        ts.pop(idx - 1)
    return weirdest


def groundHog():
    global switches, weirdRatio
    hasSwitched = False

    while True:
        tmp = input()
        if (tmp == "STOP"):
            break
        ts.append(float(tmp))
        storeWeirdRatio()
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
    if (len(ts) < period):
        exit(84)
    print("Global tendency switched %d times" % switches)
    print("5 weirdest values are", getOutliers())
except:
    exit(84)