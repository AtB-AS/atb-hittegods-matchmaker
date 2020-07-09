# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 13:15:14 2020

@author: gauhol
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import Mathing
import datetime




def getDataFrame(fileLocation):
    datafile=open(fileLocation,'r')
    df = pd.read_csv(datafile,sep='\t',skiprows=(0),header=(0))
    return df

def generateRandomDataPoint(df,i):
    
    randomValues=[]
    columnNames=list(df.columns)
    

    for colName in columnNames:
        values=df[colName].tolist()
        values=removeEmptyFromList(values)
        randomValue=generateRandomValue(values)
        
        if(colName=='foundid'):
            randomValues.append(i)
        
        elif(colName=='date'):
            date_arr=randomValue.split('/')
            date=datetime.date(int(date_arr[2]),int(date_arr[1]),int(date_arr[1]))
            randomValues.append(date)
        
        elif 'id' in colName and colName!='lineid':
            value=int(randomValue)
            randomValues.append(value)
        
        else:
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
        newDFDict.update({str(i):generateRandomDataPoint(df,i)})
    newDF=pd.DataFrame.from_dict(newDFDict, orient='index', columns=columnNames)
    return newDF

def generateDataSet(inputFile, outputFile,n):
    columnNameValues = getDataFrame(inputFile)

    dataSet=generateRandomDF(columnNameValues,n)
    dataSet.to_csv('Data/'+outputFile,sep='\t',index_label='foundid')


def testMatching():
    inputFile='Constants/ColumnsAndValuesData.txt'
    columnNameValues = getDataFrame(inputFile)
    
    dataSet=generateRandomDF(columnNameValues,100)
    columnNames=list(dataSet.columns)
    x_columnNames=columnNames
    x_columnNames.remove('foundid')
    x_columnNames.insert(0,'lostid')
    
    
    x_values=list(dict(dataSet.iloc[0]).values())
    x_dict = { x_columnNames[i] : x_values[i]  for i in range(len(x_columnNames))}

    x=pd.DataFrame(x_dict, index=[0])
    
    
    print(dataSet.head())
    print(x.head())
    print(type(x))
    
    Mathing.doMatching(x,dataSet,5)
    
    
    
    
    
    
    
    
    