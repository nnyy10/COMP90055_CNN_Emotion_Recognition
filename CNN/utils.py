import cv2
import keras
import numpy as np
import matplotlib.pyplot as plt
from mtcnn import MTCNN
import pycm
import numbers
import imblearn


def detect_faces(image):
    detector = MTCNN()
    faces = [face["box"] for face in detector.detect_faces(image)]
    return faces


def getxywh(face):
    return face[0], face[1], face[2], face[3]


def display_all_faces(image, faces):
    for face in faces:
        box_x, box_y, box_w, box_h = getxywh(face)
        image = cv2.rectangle(image, (box_x, box_y), (box_x + box_w, box_y + box_h), (255, 0, 0))

    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()


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


def down_sample(x, y):
    undersampler = imblearn.under_sampling.RandomUnderSampler(sampling_strategy="not minority", random_state=0)
    return undersampler.fit_resample(x, y)
