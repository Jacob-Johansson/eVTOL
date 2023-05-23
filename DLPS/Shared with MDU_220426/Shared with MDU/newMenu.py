import csv
import math
from CalcAndCollect import *
from barometer_get_pressure import get_pressure


def writeToFileHeader(rawErrorWriter):
    rawErrorWriter.writerow(["Row", "Iteration", "Estimated x", "Estimated y", "Estimated z", "Delta distance 1", "delta distance 2", "Delta distance 3", "Delta distance 4", "Delta distance 5", "b1posX", "b1posY", "b1posZ",  "b2posX", "b2posY", "b2posZ",  "b3posX", "b3posY", "b3posZ",  "b4posX", "b4posY", "b4posZ",  "b5posX", "b5posY", "b5posZ",  "b6posX", "b6posY", "b6posZ", "Pressure", "Actual x", "Actual y", "Actual z"])

def writeToFile(row, iteration, estimatedX, estimatedY, estimatedZ, ddist1, ddist2, ddist3, ddist4, ddist5, b1posX, b1posY, b1posZ, b2posX, b2posY, b2posZ,  b3posX, b3posY, b3posZ, b4posX, b4posY, b4posZ, b5posX, b5posY, b5posZ, b6posX, b6posY, b6posZ, pressure, actualX, actualY, actualZ):
    with open('dataset.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([str(row), str(iteration), str(estimatedX), str(estimatedY), str(estimatedZ), str(ddist1), str(ddist2), str(ddist3), str(ddist4), str(ddist5), str(b1posX), str(b1posY), str(b1posZ), str(b2posX), str(b2posY), str(b2posZ), str(b3posX), str(b3posY), str(b3posZ), str(b4posX), str(b4posY), str(b4posZ), str(b5posX), str(b5posY), str(b5posZ), str(b6posX), str(b6posY), str(b6posZ), str(pressure), str(actualX), str(actualY), str(actualZ)])

def getZValues():
    with open('generatedPositions.csv', 'r') as file:
        dataList = list(csv.reader(file))

        i =int(input("Enter which row you want to start on: "))
        dataList=dataList[(i-1):]
        #Anchors' z position
        anchorsZPosition = [0.87,0.47,1.37,0.67,0.27,1.67]
        rawErrorFileHandler = open('dataset.csv', 'w', newline='')
        rawErrorWriter = csv.writer(rawErrorFileHandler)
        if (i==1):
            writeToFile("Row", "Iteration", "Estimated x", "Estimated y", "Estimated z", "Delta distance 1", "delta distance 2", "Delta distance 3", "Delta distance 4", "Delta distance 5", "b1posX", "b1posY", "b1posZ",  "b2posX", "b2posY", "b2posZ",  "b3posX", "b3posY", "b3posZ",  "b4posX", "b4posY", "b4posZ",  "b5posX", "b5posY", "b5posZ",  "b6posX", "b6posY", "b6posZ", "Pressure", "Actual x", "Actual y", "Actual z")

        #Write header if it is first row
        for row in dataList:

            input("Confirm position (X: " + row[0] + " Y: " + row[1] + " Z: " + str(round(float(row[2]) - 0.17,2)) + ")")
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
                writeToFile(i, index, values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[9], values[10], values[11], values[12], values[13],values[14], values[15], values[16], values[17], values[18], values[19], values[20], values[21], values[22], values[23], values[24], values[25], pressure, row[0], row[1], row[2])
                index += 1
            i+=1

        
getZValues()