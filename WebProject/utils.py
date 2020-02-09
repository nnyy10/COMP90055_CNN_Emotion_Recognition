import json

import keras
import os
import numpy as np
import matplotlib.pyplot as plt
import numbers
from collections import Counter
import tensorflow as tf


emotions = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]


def emotion_int_to_str(emotion_int):
    return emotions[emotion_int]


def emotion_str_to_int(emotion_str):
    if emotion_str.lower() == "angry":
        return 0
    elif emotion_str.lower() == "disgust":
        return 1
    elif emotion_str.lower() == "fear":
        return 2
    elif emotion_str.lower() == "happy":
        return 3
    elif emotion_str.lower() == "sad":
        return 4
    elif emotion_str.lower() == "surprise":
        return 5
    elif emotion_str.lower() == "neutral":
        return 6
    else:
        return None


def get_predicted_emotion(emotion_array):
    emotion_int = np.argmax(emotion_array)
    return emotion_int_to_str(emotion_int)


def get_predicted_emotion_dictionary(emotion_array):
    dictionary = {}
    for i in range(7):
        dictionary[emotion_int_to_str(i)] = str(round(emotion_array[i], 2))
    return dictionary


def y_single_to_list(y_single):
    new_y_list = []
    for y in y_single:
        new_y = np.zeros(7)
        new_y[y] = 1
        new_y_list.append(new_y)
    return np.asarray(new_y_list)


def y_list_to_single(y_list):
    return np.asarray(list(map(np.argmax, y_list)))


def get_class_num(y_list):
    result = Counter(y_list)
    class_counter = [result[x] for x in range(7)]
    return np.asarray(class_counter)


def plot_acc_history(history):
    # summarize history for accuracy
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()


def plot_loss_history(history):
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()


def load_data_from_npy(base_directory):
    x_train = np.load(os.path.join(base_directory, 'x_train.npy'))
    x_test = np.load(os.path.join(base_directory, 'x_test.npy'))
    x_valid = np.load(os.path.join(base_directory, 'x_valid.npy'))

    y_train = np.load(os.path.join(base_directory, 'y_train.npy'))
    y_test = np.load(os.path.join(base_directory, 'y_test.npy'))
    y_valid = np.load(os.path.join(base_directory, 'y_valid.npy'))

    return x_train, y_train, x_valid, y_valid, x_test, y_test


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)