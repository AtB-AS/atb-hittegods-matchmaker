# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:36:15 2020

@author: gauhol
"""
import pandas as pd
import matplotlib.pyplot as plt
from collections import OrderedDict
from operator import itemgetter
import columns
import compare
import Weights
from Match import Match
from Entry import Entry
from dataset import dataset
from utils import getDataFrame

def doMatching(x, data, n):

    matches=Matching(x,data,n)

    if x.type == 'found':
        x.df = columns.renameContactColumns(x.df)
    else:
        data.df = columns.renameContactColumns(data.df)

    return matches



def Matching(x_dataset,y_dataset,n):

    weightMatrix = Weights.getWeightMatrix()
    valueLabels = columns.getValueLabels()

    x_row = columns.getRowValues(0,x_dataset.df,x_dataset.type)
    x = Entry(x_row[0],x_row.remove(x_row[0]))

    scores = []
    y_ids = []
    for i in range(len(y_dataset)):
        y_row = columns.getRowValues(i,y_dataset,y_dataset.type)
        y = Entry(y_row[0],y_row.remove(y_row[0]))
        try:
            scores.append(round(calculateSimilarity(weightMatrix,compareEntries(x.values,y.values,valueLabels)),3))
            y_ids.append(y.id)
        except Exception as e:
            print(e)

    [bestMatches, bestScores] = findBestMatches(scores, y_ids, n, plot=False)

    matches = []
    for i in range(0, len(bestMatches)):
        if x_dataset.type == "lost":
            matches.append(Match(x.id, bestMatches[i], bestScores[i]))
        else:
            matches.append(Match(bestMatches[i], x.id, bestScores[i]))

    return matches


def compareEntry(x,y,label):
    return compare.compare(x, y, label)


def compareEntries(x,y,labels):
    values=[]
    for i in range(len(x)):
        values.append(compareEntry(x[i],y[i],labels[i]))
    return values


def applyWeights(weights,values):
    weightedValues=[]
    for i in range(len(values)):
        weightedValues.append(weights[i]*values[i])
    return weightedValues


def calculateSimilarity(weightMatrix,values):
    
    weights=Weights.calculateWeights(values, weightMatrix)
    values=applyWeights(weights, values)

    top=0
    bottom=0
    for i in range(len(values)):
        top+=values[i]
        bottom+=max(weights[i],values[i]*weights[i])
    
    s=top/bottom
    return s

def findBestMatches(s,ref,n,plot=False):
    
    refS={ref[i]:s[i] for i in range(len(ref))}
    sortedRefS=OrderedDict(sorted(refS.items(), key = itemgetter(1), reverse = True))
    sortedRef=list(sortedRefS.keys())
    sortedS=list(sortedRefS.values())
    bestMatches=[sortedRef[i] for i in range(n)]
    bestS=[sortedS[i] for i in range(n)]

    if(plot):
        plt.figure()
        plt.bar(list(refS.keys()),list(refS.values()))
        plt.figure()
        plt.bar([i for i in range(len(refS))], list(sortedRefS.values()))
    

    return [bestMatches,bestS]


def lostOrFound(df):
    
    if('lostid' in list(df.columns)):
        return 'lost'
    elif('foundid' in list(df.columns)):
        return 'found'
    else:
        return None
