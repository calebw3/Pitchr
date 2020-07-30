# tensorflow requires 64-bit python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Flatten, Dropout
import pandas as pd
import numpy as np
from pitchr import data
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

DATA_PATH = "../dataset/_xml_scores"


# steps to NN model: 1) build model, 2) compile model, 3) train model, 4) evaluate model, 5) make predictions


def load_data(data_path):
    """Loads training dataset from xml_parser.

        :param data_path (str): Path to xml file containing data
        :return list_melody_dfs (list of dataframes): Inputs to model
        :return list_harmony_dfs (list of dataframes): Targets for model
    """

    list_melody_dfs, list_harmony_dfs = data.get_tagged_data()
    return list_melody_dfs, list_harmony_dfs


def prepare_data(test_size, validation_size):
    """Loads data and splits it into train, validation, and test sets.
        :param test_size (float): float between [0, 1] indicating percentage of data set to allocate to testing
        :param validation_size (float): float between [0, 1] indicating percentage of data set to allocate to validating

        :return melody_train (ndarray): input training set
        :return melody_validation (ndarray): input validation set
        :return melody_test (ndarray): input test set
        :return harmony_train (ndarray): target training set
        :return harmony_validation (ndarray): target validation set
        :return harmony_test (ndarray): target test set
    """
    # Load data
    list_melody_dfs, list_harmony_dfs = load_data(DATA_PATH)

    # transform dataframes into numpy arrays
    for i in range(0, len(list_melody_dfs)):
        temp_melody_df = list_melody_dfs[i]
        temp_harmony_df = list_harmony_dfs[i]
        temp_melody_df = temp_melody_df[['Pitch Number', 'Pitch Interval', 'Pitch Predictability']]
        temp_harmony_df = temp_harmony_df[['Pitch Number', 'Pitch Interval', 'Pitch Predictability']]
        temp_melody_np = temp_melody_df.to_numpy()
        temp_harmony_np = temp_harmony_df.to_numpy()
        list_melody_dfs[i] = temp_melody_np
        list_harmony_dfs[i] = temp_harmony_np

    # convert lists into 3d numpy arrays
    list_melody_dfs = np.array(list_melody_dfs)
    list_harmony_dfs = np.array(list_harmony_dfs)

    # split data
    melody_train, melody_test, harmony_train, harmony_test = train_test_split(list_melody_dfs, list_harmony_dfs,
                                                                              test_size=test_size)
    melody_train, melody_validation, harmony_train, harmony_validation = train_test_split(melody_train, harmony_train,
                                                                                          test_size=validation_size)

    return melody_train, melody_validation, melody_test, harmony_train, harmony_validation, harmony_test


def build_model():
    """Builds RNN-LSTM model

        :return model: RNN-LSTM model
    """
    model = Sequential()

    # 2 LSTM layers
    model.add(LSTM(512, input_shape=(None, 3), return_sequences=True))
    # model.add(LSTM(128, batch_input_shape=(None, None, 3), return_sequences=True))
    model.add(LSTM(512))

    # Dense layers
    model.add(Dense(64, activation="relu"))
    model.add(Dropout(0.3))

    # Output Layer
    model.add(Dense(3, activation="softmax"))
    model.summary()
    return model


def plot_history(history):
    """Plots accuracy/loss for training/validation set as a function of the epochs
        :param history: Training history of model
        :return:
    """
    fig, axs = plt.subplots(2)

    # create accuracy sublpot
    axs[0].plot(history.history["accuracy"], label="train accuracy")
    axs[0].plot(history.history["val_accuracy"], label="test accuracy")
    axs[0].set_ylabel("Accuracy")
    axs[0].legend(loc="lower right")
    axs[0].set_title("Accuracy eval")

    # create error sublpot
    axs[1].plot(history.history["loss"], label="train error")
    axs[1].plot(history.history["val_loss"], label="test error")
    axs[1].set_ylabel("Error")
    axs[1].set_xlabel("Epoch")
    axs[1].legend(loc="upper right")
    axs[1].set_title("Error eval")

    plt.show()


if __name__ == "__main__":
    # dataframe columns are:
    # Index(['Key', 'Clef', 'Letter', 'Octave', 'Accidental', 'Duration', 'Pitch',
    # 'Pitch Number', 'Pitch Interval', 'Pitch Predictability']

    """
    # get data and split data
    melody_train, melody_validation, melody_test, harmony_train, harmony_validation, harmony_test = prepare_data(0.25, 0.2)

    # build model
    print("melody_train.shape:", melody_train.shape)
    input_shape = (melody_train.shape[1], melody_train.shape[2])
    print("input_shape:", input_shape)
    model = build_model(input_shape)

    # compile model
    optimizer = keras.optimizers.Adam(learning_rate=0.0001)
    model.compile(optimizer=optimizer, loss="sparse_categorical_crossentropy", metrics=["accuracy"])

    model.summary() # summarizes model. Good for debugging

    # train model
    trained_model = model.fit(melody_train, harmony_train, validation_data=(melody_validation, harmony_validation),
              epochs=50,
              batch_size=32) # 32 is the default. Might play around with some of the parameters

    trained_model.summary()

    # plot accuracy/error for training and validation
    plot_history(trained_model)

    # evaluate model on test set
    test_loss, test_acc = model.evaluate(melody_test, harmony_test, verbose=2)
    print("Test loss:", test_loss)
    print("Test accuracy:", test_acc)
    """