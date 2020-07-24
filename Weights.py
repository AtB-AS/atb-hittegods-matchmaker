# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 14:19:56 2020

@author: gauhol
"""
import numpy as np
import matplotlib.pyplot as plt

def read_weights_from_file():
    """
    Reads the 4 weight matrixes from ./Constants/weightMatrix.txt and puts them in dict. Each matrix is a numpy array.

    :return:
    """


    params=10
    W_pp=np.loadtxt('Constants/weightMatrix.txt',skiprows=2,max_rows=params,usecols=range(params))
    W_pn=np.loadtxt('Constants/weightMatrix.txt',skiprows=2+1*(1+params),max_rows=params,usecols=range(params))
    W_np=np.loadtxt('Constants/weightMatrix.txt',skiprows=2+2*(1+params),max_rows=params,usecols=range(params))
    W_nn=np.loadtxt('Constants/weightMatrix.txt',skiprows=2+3*(1+params),max_rows=params,usecols=range(params))

    return {'W_pp':W_pp,'W_pn':W_pn,'W_np':W_np,'W_nn':W_nn}


def get_weight_matrix():
    """
    Returns weight matrix

    :return: weight matrix
    """

    return read_weights_from_file()


def calculate_weights(values, weightMatrix):
    """
    Calculates the weight for each similarity value dynamically from the weight matrix

    :param values: comparison similarity values
    :param weightMatrix: weights matrix
    :return: list of weights for each value
    """

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


def plot_weights(weightMatrix):
    """Plots weight matrixes"""
    plot_mat(weightMatrix['W_pp'], 'Weight matrix positive | positive')
    plot_mat(weightMatrix['W_pn'], 'Weight matrix positive | negative')
    plot_mat(weightMatrix['W_np'], 'Weight matrix negative | positive')
    plot_mat(weightMatrix['W_nn'], 'Weight matrix negative | negative')


def plot_mat(npArray, title):
    """Plots a weight matrix"""
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