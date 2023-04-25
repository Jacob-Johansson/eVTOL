from IPython.display import display
import pandas as pd
import math
from CalcAndCollect import *

def getZValues():
    df = pd.read_excel('AnchorHeights.xlsx')

    rowNumber = input("Row number: ")
    workingRowNumber = int(rowNumber) - 2

    iteration = input("Which iteration?")

    actualX = input("Actual X:")
    actualY = input("Actual Y:")
    actualZ = input("Actual Z:")
    actual = [actualX, actualY, actualZ]

    array = []
    for i in range(6):
        array.append(df.iloc[workingRowNumber, i])

    estimatedValues = CalcPos(array)
    index = 1
    partial = []
    w = [0,0,0]
    for i in estimatedValues:
        partial = [int(i[0])-int(actual[0]), int(i[1])-int(actual[1]), int(i[2])-int(actual[2])]
        w = [w[0]+partial[0],w[1]+partial[1],w[2]+partial[2]]
        index+=1
    finalArray = [w[0]/index, w[1]/index, w[2]/index]
    error = math.sqrt(finalArray[0]**2+finalArray[1]**2+finalArray[2]**2)
    print(error)

    #How many columns we go right
    moveRight = switch(iteration)

    df.iloc[workingRowNumber, 6+(3*moveRight)] = actualX
    df.iloc[workingRowNumber, 7+(3*moveRight)] = actualY
    df.iloc[workingRowNumber, 8+(3*moveRight)] = actualZ
    df.iloc[workingRowNumber, 21+(1*moveRight)] = error

def switch(iteration):
    if iteration == 1:
        return 0
    elif iteration == 2:
        return 1
    elif iteration == 3:
        return 2
    elif iteration == 4:
        return 3
    else:
        return 4
getZValues()