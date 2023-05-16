import numpy
import pandas

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

errorValues = errors.to_numpy()
averageValues = []

for errorRow in errorValues:
    averageValues.append(calculate_average(errorRow))

indexOfLowestMean = 0
for i in range(0, averageValues.__len__()):
    if averageValues[i] < averageValues[indexOfLowestMean]:
        indexOfLowestMean = i

anchorHeights = dataset.iloc[:, 0:6].to_numpy()
print(indexOfLowestMean)
print(anchorHeights[indexOfLowestMean])