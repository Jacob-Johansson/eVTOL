import csv
import math
from CalcAndCollect import *

def getZValues():
    #Open excel file
    with open('AnchorHeights.csv', 'r') as file, open('AvgError.csv', 'w') as outf:
        rowIndex = -1
        dataList = list(csv.reader(file))
        writer = csv.writer(outf)
        #Hide headers
        dataList=dataList[1:]
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
                rowToChange = row
                rowToChange[6 + 3*i] = actualX
                rowToChange[7 + 3*i] = actualY
                rowToChange[8 + 3*i] = actualZ
                print(rowToChange)

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
                print(error)
                #Add errors to row
                rowToChange[21 + i] = error

            #Add average error to row
            rowToChange[26] = sum(rowToChange[21:25]) / 5
            #Write row to new file
            writer.writerow(rowToChange)

getZValues()