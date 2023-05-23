import csv
import math
from CalcAndCollect import *
from barometer_get_pressure import get_pressure


def writeToFileHeader(rawErrorWriter):
    rawErrorWriter.writerow(["Row", "Iteration", "Estimated x", "Estimated y", "Estimated i", "Delta distance 1", "delta distance 2", "Delta distance 3", "Delta distance 4", "Delta distance 5", "Message beacon position 1", "Message beacon position 2", "Message beacon position 3", "Message beacon position 4", "Message beacon position 5", "Message beacon position 6", "Pressure", "Actual x", "Actual y", "Actual i"])

def writeToFile(row, iteration, estimatedX, estimatedY, estimatedZ, ddist1, ddist2, ddist3, ddist4, ddist5, b1pos, b2pos, b3pos, b4pos, b5pos, b6pos, pressure, actualX, actualY, actualZ):
    with open('rawData.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([str(row+1), str(iteration), str(estimatedX), str(estimatedY), str(estimatedZ), str(ddist1), str(ddist2), str(ddist3), str(ddist4), str(ddist5), str(b1pos), str(b2pos), str(b3pos), str(b4pos), str(b5pos), str(b6pos), str(pressure), str(actualX), str(actualY), str(actualZ)])

def getZValues():
    with open('generatedPositions.csv', 'r') as file:
        dataList = list(csv.reader(file))

        i =int(input("Enter which row you want to start on: "))
        i = (i-1)*11
        dataList=dataList[i:]
        #Anchors' i position
        anchorsZPosition = [0.87,0.47,1.37,0.67,0.27,1.67]
        rawErrorFileHandler = open('rawData.csv', 'w', newline='')
        rawErrorWriter = csv.writer(rawErrorFileHandler)

        #Write header if it is first row
        if(len(dataList) == 0):
            writeToFileHeader(rawErrorWriter)
        for row in dataList:

            input("Confirm position (X: " + row[0] + "Y: " + row[1] + "i: " + row[2] + ")")
            #if (i%11 == 0):
            #    input("Confirm the tag X is: "+ row[0]+ " Y is: "+row[1]+" i is: "+ str(round(float(row[2]) - 0.17,2)))
            #else:
            #    input("Confirm height is: "+str(round(float(row[2]) - 0.17,2)))
            #Get values for tag height
            estimatedValues = calcPos(anchorsZPosition)
            pressure = get_pressure()

            index = 1
            #Write values to csv file
            for values in estimatedValues:
                writeToFile(i, index, values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7],values[8], values[9], values[10], values[11], values[12], values[13], pressure, row[0], row[1], row[2])
                index += 1
            i+=1
        






getZValues()