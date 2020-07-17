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


def compareEntry(x,y,label):
    return compare.compare(x, y, label)


def compareEntries(x1,x2,labels):
    values=[]
    for i in range(len(x1)):
        values.append(compareEntry(x1[i],x2[i],labels[i]))
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


def getDataFrame(fileLocation):
    datafile=open(fileLocation,'r')
    df = pd.read_csv(datafile,sep='\t',skiprows=(0),header=(0))
    return df


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


def Matching(x_df,data,n):
    weightMatrix=Weights.getWeightMatrix()

    x_type=lostOrFound(x_df)
    y_type=lostOrFound(data)

    print(list(x_df.columns))
    print(list(data.columns))

    x_df=columns.renameContactColumns(x_df)
    data=columns.renameContactColumns(data)

    print(list(x_df.columns))
    print(list(data.columns))

    s=[]
    ref=[]
    valueNames=columns.getValueLabels()
    x=columns.getRowValues(0,x_df,x_type)
    x_ref=x[0]
    x_values=x
    x_values.remove(x_ref)

    print("here")



    for i in range(len(data)):
        #dont compare ref num??

        y=columns.getRowValues(i,data,y_type)

        y_ref=y[0]
        y_values=y
        y_values.remove(y_ref)
        try:
            s.append(round(calculateSimilarity(weightMatrix,compareEntries(x_values,y_values,valueNames)),3))
            ref.append(y_ref)
        except Exception as e:
            print(e)

    [bestMatches,bestS]=findBestMatches(s, ref, n, plot=False)

    matches=[]
    for i in range(0, len(bestMatches)):
        matches.append({'ID_1':x_ref,'ID_2':bestMatches[i],'score':bestS[i]})    
        
    return matches


def testMatching():
    x=[0,'Elektronikk','Mobil','Svart', 4,'5/1/2020','Bose']
    data=getDataFrame('Data/random1000.txt')

    matches=Matching(x,data,5)
    return matches


def doMatching(x, data, n):

    matches=Matching(x,data,n)
    return matches