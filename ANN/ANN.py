import numpy
import pandas
import tensorflow as tf


# Function for creating an ann
def create_ann(units, activations, input_shape):
    ann = tf.keras.models.Sequential()
    ann.add(tf.keras.layers.Dense(units=units[0], activation=activations[0], input_shape=input_shape))

    for i in range(1, len(units)):
        ann.add(tf.keras.layers.Dense(units[i], activation=activations[i]))

    return ann


# Import the Keras libraries and packages
import keras
from keras.models import Sequential
from keras.layers import Dense

print(tf.__version__)

dataset = pandas.read_csv('finalDataset.csv')
dataset.head()

from sklearn.utils import shuffle

dataset = shuffle(dataset)

actuals = dataset.loc[:, ['Actual x', 'Actual y', 'Actual z']]
estimated = dataset.loc[:,
            ['Estimated x', 'Estimated y', 'Estimated z', 'Delta distance 1', 'delta distance 2', 'Delta distance 3',
             'Delta distance 4', 'Delta distance 4']]

x = estimated.values
y = actuals.values

x = abs(x)

# split the dataset into train and test set
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

# Scale the features
from sklearn.preprocessing import StandardScaler

sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

# Create the ann's to compare
input_shape = x_train[0].shape

ann_array = [
    create_ann([512, 512, 3], [tf.keras.activations.tanh, tf.keras.activations.relu, tf.keras.activations.relu], input_shape),
    create_ann([9, 9, 3], [tf.keras.activations.tanh, tf.keras.activations.relu, tf.keras.activations.relu], input_shape),
    create_ann([9, 3], [tf.keras.activations.tanh, tf.keras.activations.relu], input_shape)
]

num_epochs = 90

history_array = []

# Visualize the model
#from tensorflow.keras.utils import plot_model
#plot_model(ann, to_file="model.png", show_shapes=True, show_layer_names=True, )

# Train the ann's
for i in range(0, len(ann_array)):
    ann_array[i].compile(optimizer='sgd', loss=tf.keras.losses.MeanSquaredError(), metrics=[tf.keras.metrics.MeanSquaredError()])
    history_array.append(ann_array[i].fit(x_train, y_train, epochs=num_epochs, validation_split=0.1, callbacks=[tf.keras.callbacks.LearningRateScheduler(lambda epoch: 1e-3 * 10 ** (epoch / 30))]))

# Visualize & evaluate the model
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['figure.figsize'] = (18, 8)
rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False

# Evaluate the model
import csv

for i in range(0, len(ann_array)):
    history = history_array[i]
    ann = ann_array[i]

    print(history.history.keys())

    # Evaluate the model
    y_predicted = ann.predict(x_test)
    tb = pandas.DataFrame(list(zip(y_test, y_predicted)), columns=['Actual', 'Predicted'])
    tb.to_csv('predicted_vs_actual'+str(i)+'.csv')

# Plot Mean Square Error, Loss, learning rate and epoch
plt.subplot(1, 2, 1)
for i in range(0, len(ann_array)):
    history = history_array[i]
    ann = ann_array[i]

    #plt.plot(
    #    numpy.arange(1, num_epochs + 1),
    #    history.history['loss'],
    #    label='Loss '+str(i), lw=3
    #)
    plt.plot(
        numpy.arange(1, num_epochs + 1),
        history.history['val_loss'],
        label='Validation loss'+str(i), lw=3
    )

    plt.plot(
        numpy.arange(1, num_epochs + 1),
        history.history['mean_squared_error'],
        label='Mean Square Error '+str(i), lw=3
    )
    #plt.plot(
    #    numpy.arange(1, num_epochs + 1),
    #    history.history['lr'],
    #    label='Learning rate '+str(i), color='#000', lw=3, linestyle='--'
    #)
    plt.title('Evaluation metrics', size=18)
    plt.xlabel('Epoch', size=14)
    plt.legend()

# Plot learning rate to loss
plt.subplot(1, 2, 2)
for i in range(0, len(ann_array)):
    history = history_array[i]
    ann = ann_array[i]

    learning_rates = 1e-3 * (10 ** (numpy.arange(num_epochs) / 30))
    plt.semilogx(
        learning_rates,
        history.history['loss'],
        lw=3, label='Loss'+str(i)
    )
    plt.title('Learning rate vs. Mean Square Error', size=18)
    plt.xlabel('Learning rate', size=14)
    plt.ylabel('Mean Square Error', size=14)
    plt.legend()

# set the spacing between subplots
plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.4)
plt.show()
