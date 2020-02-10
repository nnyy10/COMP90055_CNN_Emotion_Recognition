import base64
import json

import keras
import os
import numpy as np
import matplotlib.pyplot as plt
import numbers
from collections import Counter
import tensorflow as tf
from PIL import Image
import io
import cv2

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
    emotion_structured = []
    for i in range(7):
        emotion_structured.append({"emotion": emotion_int_to_str(i), "probability": str(round(emotion_array[i], 2))})
    emotion_structured = sorted(emotion_structured, key=lambda x: x['probability'], reverse=True)
    return emotion_structured


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

def stringToRGB(base64_string):
    imgdata = base64.b64decode(str(base64_string))
    image = Image.open(io.BytesIO(imgdata))
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

def rgbToString(BGR_array):
    print(type(BGR_array))
    print(BGR_array.shape)
    im_rgb = BGR_array[:, :, [2, 1, 0]]
    pil_img = Image.fromarray(im_rgb.astype('uint8'))

    buff = io.BytesIO()
    pil_img.save(buff, format="JPEG")
    return base64.b64encode(buff.getvalue()).decode("utf-8")
