# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:36:15 2020

@author: gauhol
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from collections import OrderedDict
from operator import itemgetter


#TODO forskjellig vekting for positiv og negativ correlation



def compareEntry(x,y):
    if(x==y):
        return 1
    else:
        return 0
    
def compareEntries(x1,x2):
    values=[]
    for i in range(len(x1)):
        values.append(compareEntry(x1[i],x2[i]))
    
    return values

def applyWights(weights,values):
    weightedValues=[]
    for i in range(len(weights)):
        weightedValues.append(weights[i]*values[i])
    return weightedValues
        


def calculateSimilarity(weights,values):
    
    values=applyWights(weights, values)

    top=0
    bottom=0
    for i in range(len(values)):
        top+=values[i]
        bottom+=weights[i]
    
    s=(top)/bottom
    
    return s
    
def getWeights():
    weights=[1,1,1,1,1,1]
    return weights

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
    
    

def Matching(x,data,n):
    weights=getWeights()
    
    s=[]
    ref=[]
    
    x_values=x.remove(x[len(x)-1])
    
    x_ref=x[0]
    

    for i in range(len(data)):
        #dont compare ref num??
        
        y=list(dict(data.iloc[i]).values())
        
        
        y_ref=y[0]
        y_values=y.remove(y[len(y)-1])
        s.append(round(calculateSimilarity(weights,compareEntries(x,y)),3))
        ref.append(y_ref)
        
    
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



























