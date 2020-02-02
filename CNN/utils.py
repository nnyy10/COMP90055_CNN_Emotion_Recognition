import cv2
import keras
import os
import numpy as np
import matplotlib.pyplot as plt
import pycm
import numbers
import imblearn
from collections import Counter
import tensorflow as tf
from face_detection import getxywh


def emotion_int_to_str(emotion_int):
    if emotion_int == 0:
        return "Angry"
    elif emotion_int == 1:
        return "Disgust"
    elif emotion_int == 2:
        return "Fear"
    elif emotion_int == 3:
        return "Happy"
    elif emotion_int == 4:
        return "Sad"
    elif emotion_int == 5:
        return "Surprise"
    elif emotion_int == 6:
        return "Neutral"
    else:
        return None


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


def process_face(image, face):
    box_x, box_y, box_w, box_h = getxywh(face)
    crop_img = image[box_y:box_y + box_h, box_x:box_x + box_w]
    gray_img = cv2.cvtColor(crop_img, cv2.COLOR_RGB2GRAY)
    resized = cv2.resize(gray_img, (160, 160))
    resized = np.true_divide(resized, 255)
    stacked_img = np.stack((resized,) * 3, axis=-1)
    return stacked_img


def get_predicted_emotion(emotion_array):
    emotion_int = np.argmax(emotion_array)
    if emotion_int == 0:
        return "Angry"
    elif emotion_int == 1:
        return "Disgust"
    elif emotion_int == 2:
        return "Fear"
    elif emotion_int == 3:
        return "Happy"
    elif emotion_int == 4:
        return "Sad"
    elif emotion_int == 5:
        return "Surprise"
    elif emotion_int == 6:
        return "Neutral"
    else:
        return "invalid emotion"


def load_model(model):
    return keras.models.load_model(model)


def y_single_to_list(y_single):
    new_y_list = []
    for y in y_single:
        new_y = np.zeros(7)
        new_y[y] = 1
        new_y_list.append(new_y)
    return np.asarray(new_y_list)


def y_list_to_single(y_list):
    return np.asarray(list(map(np.argmax, y_list)))


def print_confusion_matrix(y_predicted, y_actual):
    if len(y_predicted) > 0 and len(y_actual) > 0:
        if not isinstance(y_actual[0], numbers.Number):
            y_actual = y_list_to_single(y_actual)
        if not isinstance(y_predicted[0], numbers.Number):
            y_predicted = y_list_to_single(y_predicted)
        print(pycm.ConfusionMatrix(actual_vector=y_actual, predict_vector=y_predicted))
    else:
        print("invalid input")


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

def under_sample(x, y):
    under_sampler = imblearn.under_sampling.RandomUnderSampler(sampling_strategy="not minority", random_state=42)
    return under_sampler.fit_resample(x, y)


def up_sample_smote(x, y):
    sm = imblearn.over_sampling.SMOTE(random_state=42)
    return sm.fit_resample(x, y)


def load_data():
    base_image_path = 'data/processed_data'
    image_type_path = 'base'

    x_train = np.load(os.path.join(base_image_path, image_type_path, 'x_train.npy'))
    # x_train_new = []
    # for x in x_train:
    #     x_train_new.append(cv2.resize(x, (160, 160)))
    # x_train = np.array(x_train_new)
    x_train = np.true_divide(x_train, 255)

    x_test_new = []
    x_test = np.load(os.path.join(base_image_path, image_type_path, 'x_test.npy'))
    # for x in x_test:
    #     x_test_new.append(cv2.resize(x, (160, 160)))
    # x_test = np.array(x_test_new)
    x_test = np.true_divide(x_test, 255)

    x_valid_new = []
    x_valid = np.load(os.path.join(base_image_path, image_type_path, 'x_valid.npy'))
    # for x in x_valid:
    #     x_valid_new.append(cv2.resize(x, (160, 160)))
    # x = np.array(x_valid_new)
    x_valid = np.true_divide(x_valid, 255)

    y_train = np.load(os.path.join(base_image_path, image_type_path, 'y_train.npy'))
    y_test = np.load(os.path.join(base_image_path, image_type_path, 'y_test.npy'))
    y_valid = np.load(os.path.join(base_image_path, image_type_path, 'y_valid.npy'))

    return x_train, y_train, x_valid, y_valid, x_test, y_test

def create_model():
    model_dir = 'model/keras/model/facenet_keras.h5'

    inception_v1_model = keras.models.load_model(model_dir)
    cnt = 0
    for layer in inception_v1_model.layers:
        if cnt == 200:
            break
        layer.trainable = False
        cnt += 1


    model = keras.Sequential()

    model.add(inception_v1_model)
    model.add(keras.layers.Dense(7, activation='softmax'))
    print(model.summary())

    model.compile(keras.optimizers.RMSprop(lr=0.00001), metrics=['accuracy'],
                  loss=tf.keras.losses.categorical_crossentropy)
    return model
