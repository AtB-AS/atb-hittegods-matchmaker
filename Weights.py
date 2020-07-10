# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 14:19:56 2020

@author: gauhol
"""
import numpy as np
import matplotlib.pyplot as plt

def readWeightsFromFile():
    W_pp=np.loadtxt('Constants/weightMatrix.txt',skiprows=2,max_rows=7,usecols=range(7))
    W_pn=np.loadtxt('Constants/weightMatrix.txt',skiprows=10,max_rows=7,usecols=range(7))
    W_np=np.loadtxt('Constants/weightMatrix.txt',skiprows=18,max_rows=7,usecols=range(7))
    W_nn=np.loadtxt('Constants/weightMatrix.txt',skiprows=26,max_rows=7,usecols=range(7))

    return {'W_pp':W_pp,'W_pn':W_pn,'W_np':W_np,'W_nn':W_nn}


def getWeightMatrix():
    return readWeightsFromFile()


def calculateWeights(values,weightMatrix):
    k=0.5 #threshold
    N=len(values)
    weights=[]
    for i in range(N):
        x=values[i]
        w=[]
        for j in range(N):
            y=values[j]
            if(x>=k and y>=k):
                w.append(weightMatrix['W_pp'][i][j])
            elif(x>=k and y<k):
                w.append(weightMatrix['W_pn'][i][j])
            elif(x<k and y>=k):
                w.append(weightMatrix['W_np'][i][j])
            elif(x<k and y<k):
                w.append(weightMatrix['W_nn'][i][j])
        weights.append(sum(w)/N)
    return weights


def plotWeights(weightMatrix):
    plotMat(weightMatrix['W_pp'],'Weight matrix positive | positive')
    plotMat(weightMatrix['W_pn'],'Weight matrix positive | negative')
    plotMat(weightMatrix['W_np'],'Weight matrix negative | positive')
    plotMat(weightMatrix['W_nn'],'Weight matrix negative | negative')


def plotMat(npArray,title):
    labels=['catid', 'subcatid', 'brand','date','lineid','colorid','description']
    fig=plt.figure()
    ax = plt.gca()
    im=ax.matshow(npArray);
    fig.colorbar(im)
    ax.set_xticks(np.arange(7))
    ax.set_xticklabels(labels)
    ax.set_yticks(np.arange(7))
    ax.set_yticklabels(labels)
    plt.setp([tick.label2 for tick in ax.xaxis.get_major_ticks()], rotation=45,
    ha="left", va="center",rotation_mode="anchor")
    ax.set_title(title, pad = 40)
    fig.tight_layout()