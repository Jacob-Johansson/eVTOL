import csv
import math
from CalcAndCollect import *

def writeToFile(row):
    with open('outputFile.csv', 'a',newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(row)


def getZValues():
    #Open excel file
    with open('AnchorHeights.csv', 'r') as file:
        rowIndex = -1
        dataList = list(csv.reader(file))
        print(dataList[0])
        writeToFile(dataList[0])
        #Hide headers
        z=int(input("Enter which row you want to start on: "))
        dataList=dataList[z:]
        rowToCHange = []
        for row in dataList:
        #for row in range(0,2):
            rowIndex += 1
            for i in range(0, 5):
                print('Row: ' + str(rowIndex + 1) +  ' Iteration: ' + str(i + 1))


                #Take z values of anchors from csv file
                array = []
                for column in range(0,6):
                    array.append(float(dataList[rowIndex][column]))
                print(array)
                
                #Ask for actual X,Y,Z of the drone
                actualX = input("Actual X:")
                actualY = input("Actual Y:")
                actualZ = input("Actual Z:")
                actual = [actualX, actualY, actualZ]

                #SUBJECT TO CHANGE: KEEPING ACTUAL XYZ FOR ALL 5 POSITIONS MOST LIKELY NOT NEEDED
                #Write actual XYZ to csv file 
                rowToWrite = row
                rowToWrite[6 + 3*i] = actualX
                rowToWrite[7 + 3*i] = actualY
                rowToWrite[8 + 3*i] = actualZ
                print(rowToWrite)
                #print(sum(rowToWrite[21:25]))

                #Get estimated value from function passing array as argument
                estimatedValues = CalcPos(array)

                #Calculate error
                index = 1
                partial = []
                w = [0,0,0]
                for j in estimatedValues:
                    partial = [int(j[0])-int(actual[0]), int(j[1])-int(actual[1]), int(j[2])-int(actual[2])]
                    w = [w[0]+partial[0],w[1]+partial[1],w[2]+partial[2]]
                    index+=1
                finalArray = [w[0]/index, w[1]/index, w[2]/index]
                error = math.sqrt(finalArray[0]**2+finalArray[1]**2+finalArray[2]**2)
                #print(error)
                #Add errors to row
                rowToWrite[21 + i] = str(error)

            #Add average error to row
            sumError = 0
            for k in range(0,5):
                sumError += float(rowToWrite[21 + k])
                print(rowToWrite[21 + k])

            avgError = sumError / 5
            rowToWrite[26] = str(avgError)
            print(rowToWrite[0])
            #Write row to new file
            writeToFile(rowToWrite)
getZValues()