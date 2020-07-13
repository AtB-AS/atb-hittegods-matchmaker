# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 14:41:35 2020

@author: gauhol
"""

import datetime
import math
import numpy as np


def compare(x, y, label):

    # TODO what if x or y is none?

    if label == "catid" or label == "subcatid" or label == "colorid":
        if str(x).isdigit() and str(y).isdigit():
            return compareID(x, y)

    elif label == "lineid":
        if str(x).isdigit():
            x = str(x)
        if str(y).isdigit():
            y = str(y)

        if checkType(x, y, str, label):
            return compareLine(x, y)

    elif label == "brand":
        if checkType(x, y, str, label):
            return compareBrand(x, y)

    elif label == "date":
        if checkType(x, y, datetime.date, label):
            return compareDate(x, y)

    elif label == "description":
        if checkType(x, y, str, label):
            return compareDescription(x, y)

    return 0


def checkType(x, y, theType, label):
    if type(x) == theType and type(y) == theType and x != None:
        return True
    else:
        print("wrong type" + str(type(x)) + str(type(y)) + " for " + label)
        return False


def compareDescription(x, y):

    sameWord, nWords = compareWords(x, y, returnNumWords=True)

    N = nWords[0] * nWords[1]

    similarity = (sameWord / math.log(1 + N)) ** (abs(math.log(N / 2)))

    return similarity


def compareDate(x, y):

    if type(x) != datetime.date or type(y) != datetime.date:
        print("WARNING: Date not type datetime.date")
        return 0

    # Assuming type datetime.date

    timedelta = abs((x - y).days)

    if timedelta < 3:
        return 1

    return 2 / timedelta


def compareID(x, y):
    if x == y:
        return 1
    else:
        return 0


def compareLine(x, y):
    sameLine = 0

    x_arr = splitWords(x, [",", ".", ":", ";"])
    y_arr = splitWords(y, [",", ".", ":", ";"])

    for line_x in x_arr:
        for line_y in y_arr:
            if line_x == line_y:
                sameLine += 1

    # TODO Should this be evaluated differently???
    if sameLine > 0:
        return 1
    else:
        return 0


def compareBrand(x, y):

    sameWord = compareWords(x, y)

    if sameWord > 0:
        return 1
    else:
        return 0


def compareWords(x, y, returnNumWords=False):

    treshold = 0.6
    sameWord = 0
    x_arr = splitWords(x, [",", ".", ":", ";"])
    y_arr = splitWords(y, [",", ".", ":", ";"])

    for word_x in x_arr:
        for word_y in y_arr:
            if compareCharArray(word_x, word_y) > treshold:
                sameWord += 1
    if returnNumWords:
        return [sameWord, [len(x_arr), len(y_arr)]]
    else:
        return sameWord


def splitWords(x, delimeters):
    for delimeter in delimeters:
        x = x.replace(delimeter, " ")
    x_arr = x.split(" ")
    return x_arr


def compareCharArray(x, y):

    sameChar = 0
    x = x.lower()
    y = y.lower()
    x_arr = list(x)
    y_arr = list(y)

    for char_x in x_arr:
        if char_x.isdigit():
            continue
        for char_y in y_arr:
            if char_x == char_y:
                sameChar += 1

    return sameChar / max([len(x_arr), len(y_arr)])
