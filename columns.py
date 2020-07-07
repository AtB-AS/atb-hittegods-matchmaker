from csv import reader


def getColumnLabels(lost=False,found=False):

    file = open('Constants/columnLabels.txt', 'r')
    labels=file.readline().split(',')
    if(lost):
        labels.insert(0,'lostid')
    if(found):
        labels.insert(0, 'foundid')

    print("LABELS:  " + str(labels))
    file.close()
    return labels


def getRowValues(i,df,type):
    if(type=='lost'):
        labels = getColumnLabels(lost=True)
    else:
        labels = getColumnLabels(found=True)


    values=[]
    for label in labels:
        values.append(df.loc[i,label])
    return values