import numpy
import pandas

# Import the Keras libraries and packages
import keras
from keras.models import Sequential
from keras.layers import Dense

dataset = pandas.read_csv('outputFile.csv')
print(dataset)

actual = dataset.iloc[:, 6:21]
error = dataset.iloc[:, 21:27]
print(actual)
print(error)

x = pandas.DataFrame(actual)
y = error.values

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

# Build Artificial Neural Network

# Initialize the Artificial Neural Network
classifier = Sequential()
# Add the input layer and the first hidden layer
classifier.add(output_dim=6, init='uniform', activation='relu', input_dim=11)
# Add the second hidden layer
classifier.add(Dense(output_dim=6, init='uniform', activation='relu'))
# Add the output layer
classifier.add(Dense(output_dim=1, init='uniform', activation='sigmoid'))
