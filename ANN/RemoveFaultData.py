import numpy
import pandas
import csv

def setFaultyErrorToNone(errorArray):
    for i in range(0, errorArray.size):
        if errorArray[i] > 1:
            errorArray[i] = False

    return errorArray

def calculate_average(errorArray):
    output = 0

    numErrorUsed = 0
    for i in range(0, errorArray.size):
        if errorArray[i] < 100:
            output += errorArray[i]
            numErrorUsed += 1

    return output / numErrorUsed

dataset = pandas.read_csv('outputFile.csv')

errors = dataset.iloc[:, 21:26]
#print(errors)

errorValues = errors.to_numpy()

f = open('outputNonFaultyErrors.csv', 'w')
writer = csv.writer(f)
for errorRow in errorValues:
    errorRow = setFaultyErrorToNone(errorRow)
    print(errorRow)
    writer.writerow(errorRow)

f.close()



