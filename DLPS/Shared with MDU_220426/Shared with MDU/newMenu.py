import csv
import math
#from CalcAndCollect import *


def writeToFileHeader(rawErrorWriter):
    rawErrorWriter.writerow(["Row", "Iteration", "Actual x", "Actual y", "Actual z", "Estimated x", "Estimated y", "Estimated z"])

def writeToFile(row, iteration, actualX, actualY, actualZ, estimatedX, estimatedY, estimatedZ):
    with open('rawData.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([str(row+1), str(iteration), str(actualX), str(actualY), str(actualZ), str(estimatedX), str(estimatedY), str(estimatedZ)])

def getZValues():
    with open('generatedPositions.csv', 'r') as file:
        dataList = list(csv.reader(file))

        z =int(input("Enter which row you want to start on: "))
        z = (z-1)*11
        dataList=dataList[z:]
        #Anchors' z position
        anchorsZPosition = [0.87,0.47,1.37,0.67,0.27,1.67]
        rawErrorFileHandler = open('rawData.csv', 'w', newline='')
        rawErrorWriter = csv.writer(rawErrorFileHandler)

        #Write header if it is first row
        if(z == 0):
            writeToFileHeader(rawErrorWriter)
        for row in dataList:
            if (z%11 == 0):
                input("Confirm the tag X is: "+ row[0]+ " Y is: "+row[1]+" Z is: "+ str(round(float(row[2]) - 0.17,2)))
            else:
                input("Confirm height is: "+str(round(float(row[2]) - 0.17,2)))
            #Get values for tag height
            #estimatedValues = calcPos(anchorsZPosition)
            estimatedValues = [(0,0,0),(1,1,1)]
            index = 1
            #Write values to csv file
            for values in estimatedValues:
                writeToFile(z, index,row[0], row[1], row[2], values[0], values[1], values[2])
                index += 1
            z+=1
        






getZValues()