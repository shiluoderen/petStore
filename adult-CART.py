#! /usr/bin/env python
#coding=utf-8
import math

# a cartNode is a node in the CART tree
# col is a number, means the numberth attribute
# value is a number or string, means the value of the attribute
# results is a dictionary, it contains the number of points in each class 
#         if the node is not a leaf, results=None
# lb is the left son node
# rb is the right son node
class cartNode:
    def __init__(self, col=-1, value=None, results=None, lb=None, rb=None):
        self.col = col            
        self.value = value        
        self.results = results    
        self.lb = lb              
        self.rb = rb              



# readfile(String)
# Given a filename, read this file and store the data in spambase
def readfile(filename):
    f = open(filename)
    adultBase=[]
    while True:
        line=f.readline()
        if len(line)==0:
            break
        adultBase.append(line)
    f.close()
    return adultBase

# getAdultList(List)
# given a list of data, return a list of adult
def getAdultList(database):
    adultList=[]
    adult=[]
    for i in range(0,len(database)):
        adult=database[i].split(', ')
        for j in range(0,len(adult)):
            if isNumber(adult[j]):
                adult[j]=float(adult[j])
        if adult[-1]=='<=50K\n':
            adult[-1]='<=50K'
        elif adult[-1]=='>50K\n':
            adult[-1]='>50K'
        if len(adult)==15:
            adultList.append(adult)
    return adultList

# cleanList(List)
# given a List, return a List removed '?' 
def cleanList(aList):
    result=[]
    hasUnknown=False
    for adult in aList:
        for i in range(0,len(adult)):
            if adult[i]=='?':
                hasUnknown=True
        if not hasUnknown:
            result.append(adult)
        hasUnknown=False
    return result
        
# isNumber(X)
# given a X, return whether it is number or not
def isNumber(x):
    try:
        float(x)
        return True
    except:
        return False

# getPwj(List,Label)
# given a List and a Label, 
# return the probability of the Label in this List
def getPwj(aList,wj):
    Pwj=0.0
    counter=0.0
    for adult in aList:
        if adult[14]==wj:
            counter=counter+1
    Pwj=counter/len(aList)
    return Pwj

# giniImpurity(List)
# given a List, 
# return the gini impurity of this List
def giniImpurity(aList):
    result=0.0
    if len(aList)==0:
        return 0.0
    P1=getPwj(aList,'<=50K')
    P2=getPwj(aList,'>50K')
    result=1-(P1*P1+P2*P2)
    return result

# getSetLR(List, List)
# given a List of data and a stump
# return two split sets.
def getSetLR(aList,stump):
    setL=[]
    setR=[]
    if isNumber(aList[0][stump[0]]):
        for adult in aList:
            if adult[stump[0]]<stump[1]:
                setL.append(adult)
            else:
                setR.append(adult)
    else:
        for adult in aList:
            if adult[stump[0]]==stump[1]:
                setL.append(adult)
            else:
                setR.append(adult)
    return [setL,setR]
    
    
# deltaImpurity(List,List)
# given a List and a stump, 
# return the decrease of Gini Impurity
# stump=[10,40]
# stump[0]=feature #
# stump[1]=value
def deltaImpurity(aList,stump):
    result=0.0
    #sortedList=aList[:]
    setLR=[]
    setL=[]
    setR=[]
    PL=0.0
    iN=0.0
    iNL=0.0
    iNR=0.0
    setLR=getSetLR(aList,stump)
    setL=setLR[0]
    setR=setLR[1]
    iN=giniImpurity(aList)
    iNL=giniImpurity(setL)
    iNR=giniImpurity(setR)
    PL=float(len(setL))/len(aList)
    result=iN-PL*iNL-(1-PL)*iNR
    return result
    

# uniqueCounts(List)
# given a List,
# return the point number for each class            
def uniqueCounts(dataList):
    #make a dictionary of labels
    results={}
    for adult in dataList:
        # the label(y) lies in the last column
        label=adult[-1]
        if label not in results:results[label] = 0
        results[label] += 1
    return results
            
# buildTree(List,List)
# given a List of data and a List of flag
# return a CART tree
def buildTree(dataList,flagList):
    if len(dataList)==0: return cartNode()
    
    bestStump=getBestStump2(dataList,flagList)
    
    if bestStump[2]>0:
        setLR=getSetLR(dataList,bestStump)
        setL=setLR[0]
        setR=setLR[1]
        flagList[bestStump[0]]=1
        leftBranch=buildTree(setL,flagList)
        rightBranch=buildTree(setR,flagList)
        flagList[bestStump[0]]=0
        return cartNode(col=bestStump[0],value=bestStump[1],lb=leftBranch,rb=rightBranch)
    else:
        return cartNode(results = uniqueCounts(dataList))
    
# printTree(Tree)
# given a Tree, 
# convert the tree to readable format and write into a file
def printTree(tree,indent=''):
    if tree.results!=None:
        FO.write(str(tree.results)+"\n")
    else:
        FO.write(str(tree.col)+':'+str(tree.value)+'?'+'\n')
        FO.write(indent+'True->')
        printTree(tree.lb,indent+'  ')
        FO.write(indent+'False->')
        printTree(tree.rb,indent+'  ')

# initColFlag(List)
# given a List
# return a list of flag with initial value 0
def initColFlag(aList):
    colFlag=[]
    for i in range(0,len(aList)):
        colFlag.append(0)
    return colFlag
    
# predict(Adult,Tree)
# given an Adult and a decision tree,
# return whether this adult's income is <=50K or >50K 
def predict(anAdult,tree):
    if tree.results != None:
        if len(tree.results)==1:
            return tree.results.keys()[0]
        else:
            if tree.results[tree.results.keys()[0]]>tree.results[tree.results.keys()[1]]:
                return tree.results.keys()[0]
            else:
                return tree.results.keys()[1]
    else:
        helper = anAdult[tree.col]
        if isNumber(tree.value):
            if helper>=tree.value:
                branch = tree.rb
            else:
                branch = tree.lb
        else:
            if helper==tree.value:
                branch = tree.lb
            else:
                branch = tree.rb
        return predict(anAdult,branch)

# getErrRate(List,Tree)
# given a List of Adult and a decision Tree
# return the error rate 
def getErrRate(aList,tree):
    correct=0.0
    for adult in aList:
        if predict(adult,tree)==adult[-1]:
            correct=correct+1
    return 1-correct/len(aList)

# getBestStump2(List,List)
# given a List of Adult and a List of flag, 
# return the split attribute, value and reduction of Gini impurity
def getBestStump2(aList,colFlag):
    bestGain = 0.0
    bestStump = None
    bestSets = None
    setLR=[]
    
    columnCount = len(aList[0])-1
    for col in range(columnCount):
        if colFlag[col]==1:
            # if the attribute has been chosen before, skip it
            continue
        columnValues = {}
        for adult in aList:
            if len(adult)==columnCount+1:
                columnValues[adult[col]] = 1
        # for continuous value, find the best stump 
        if isNumber(aList[0][col]):
            maxValue = 0
            for value in columnValues:
                if value>maxValue:
                    maxValue = value
            value = maxValue
            while(value>1):
                setLR = getSetLR(aList,[col,value])
                setL=setLR[0]
                setR=setLR[1]
                gain=deltaImpurity(aList,[col,value])
                if gain>bestGain and len(setL)>0 and len(setR)>0:
                    bestGain = gain
                    bestStump = (col,value)
                value = int(value/1.1)
            continue
            
        #for discrete value, try one by one
        for value in columnValues:
            setLR = getSetLR(aList,[col,value])
            setL=setLR[0]
            setR=setLR[1]
            
            #infomation gain
            gain=deltaImpurity(aList,[col,value])
            if gain>bestGain and len(setL)>0 and len(setR)>0:
                bestGain = gain
                bestStump = (col,value)
    if bestGain>0:
        return [bestStump[0],bestStump[1],bestGain]
    else:
        return [None,None,0]
    
###############################################

adultBase = []
adultList = []
testBase = []
testList = []


adultBase = readfile(r'D:\pycharm\61549794CART\adult.data')
testBase = readfile(r'D:\pycharm\61549794CART\adult.test')
# adultBase = readfile('adult.data')
# testBase = readfile('adult.test')
adultList = cleanList(getAdultList(adultBase))
testList = cleanList(getAdultList(testBase))

tree=buildTree(adultList,initColFlag(adultList))
FO = open("tree.txt","w")
printTree(tree)
FO.close()

print('errRate=',getErrRate(testList,tree))