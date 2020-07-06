# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 13:15:14 2020

@author: gauhol
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random





def getDataFrame(fileLocation):
    datafile=open(fileLocation,'r')
    df = pd.read_csv(datafile,sep='\t',skiprows=(0),header=(0))
    return df

def generateRandomDataPoint(df):
    
    randomValues=[]
    columnNames=list(df.columns)
    
    
    
    for colName in columnNames:
        values=df[colName].tolist()
        values=removeEmptyFromList(values)
        randomValue=generateRandomValue(values)
        randomValues.append(randomValue)
    
      
    return randomValues

def generateRandomValue(values):
    max=len(values)
    randomIndex=random.randint(0,max-1)
    return values[randomIndex]

def removeEmptyFromList(List):
    newList=[]
    for item in List:
        if(pd.isna([item])==False):
            newList.append(item)
    return newList


def generateRandomDF(df,n):
    columnNames=list(df.columns)
    newDFDict={}
    for i in range(n):
        newDFDict.update({str(i):generateRandomDataPoint(df)})
    newDF=pd.DataFrame.from_dict(newDFDict, orient='index', columns=columnNames)
    return newDF

def generateDataSet(inputFile, outputFile,n):
    columnNameValues = getDataFrame(inputFile)

    dataSet=generateRandomDF(columnNameValues,n)
    dataSet.to_csv('Data/'+outputFile,sep='\t',index_label='ref')



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




    
    