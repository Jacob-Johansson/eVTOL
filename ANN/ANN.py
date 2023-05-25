import numpy
import pandas
import tensorflow

# Import the Keras libraries and packages
import keras
from keras.models import Sequential
from keras.layers import Dense

print(tensorflow.__version__)

dataset = pandas.read_csv('finalDataset.csv')
dataset.head()

actuals = dataset.iloc[:, 2:4]
estimated = dataset.iloc[:, 29:31]

print(actuals)

x = estimated.values
y = actuals.values

# split the dataset into train and test set
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

# Scale the features
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)
print(x_train)

# Initializing the ANN
ann = tensorflow.keras.models.Sequential()
# Add the input layer and first hidden layer
ann.add(tensorflow.keras.layers.Dense(units=9, activation=tensorflow.keras.activations.sigmoid, input_shape=x_train[0].shape))
# Add the second hidden layer
ann.add(tensorflow.keras.layers.Dense(units=8, activation=tensorflow.keras.activations.sigmoid))
# Add the output layer
ann.add(tensorflow.keras.layers.Dense(units=3, activation=tensorflow.keras.activations.sigmoid))

# Visualize the model
from tensorflow.keras.utils import plot_model
plot_model(ann, to_file="model.png", show_shapes=True, show_layer_names=True,)

# Train the ann
ann.compile(optimizer='sgd', loss=tensorflow.keras.losses.MeanSquaredError(), metrics=[tensorflow.keras.metrics.RootMeanSquaredError()])
ann.fit(x_train, y_train, epochs=100)

# Evaluate the model
y_predicted = ann.predict(x_test)
tb = pandas.DataFrame(list(zip(y_test, y_predicted)), columns=['Actual', 'Predicted'])
print(tb)